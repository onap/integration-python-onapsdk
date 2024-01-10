"""A&AI bulk module."""
#   Copyright 2022 Orange, Deutsche Telekom AG
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from dataclasses import dataclass
from re import compile as re_compile, Match, Pattern
from typing import Any, Dict, Iterable, List, Optional, TYPE_CHECKING

from more_itertools import chunked

from onapsdk.configuration import settings
from onapsdk.exceptions import APIError
from onapsdk.utils.jinja import jinja_env

from .aai_element import AaiElement

if TYPE_CHECKING:
    from jinja2 import Template


@dataclass
class AaiBulkRequest:
    """Class to store information about a request to be sent in A&AI bulk request."""

    action: str
    uri: str
    body: Dict[Any, Any]


@dataclass
class AaiBulkResponse:
    """Class to store A&AI bulk response."""

    action: str
    uri: str
    status_code: int
    body: str


class AaiBulk(AaiElement):
    """A&AI bulk class.

    Use it to send bulk request to A&AI. With bulk request you can send
        multiple requests at once.
    """

    BULK_TEMPLATE = "aai_bulk.json.j2"
    FIRST_REGEX_GROUP_NAME = "index1"
    SECOND_REGEX_GROUP_NAME = "index2"
    OPERATION_INDEX_REGEX = (fr".*((Error with operation (?P<{FIRST_REGEX_GROUP_NAME}>\d+))|"
                             fr"(Operation (?P<{SECOND_REGEX_GROUP_NAME}>\d+) with action))")

    def __init__(self,
                 chunk_size: int = settings.AAI_BULK_CHUNK) -> None:
        """Init AAI bulk class.

        Args:
            chunk_size (int, optional): How many operations are going to be send with one request.
                Defaults to settings.AAI_BULK_CHUNK.
        """
        super().__init__()
        self.chunk_size: int = chunk_size
        self._jinja_template: Optional["Template"] = None
        self._failed_requests: Optional[List[AaiBulkRequest]] = None
        self._operation_index_regex: Pattern = re_compile(self.OPERATION_INDEX_REGEX)

    @property
    def url(self) -> str:
        """Bulk url.

        Returns:
            str: A&AI bulk API url.

        """
        return f"{self.base_url}{self.api_version}/bulk"

    @property
    def jinja_template(self) -> "Template":
        """Jinja template propery.

        As we are reusing same template multiple times it's better to load it once.

        Returns:
            Template: Template of A&AI bulk request body

        """
        if not self._jinja_template:
            self._jinja_template = jinja_env().get_template(self.BULK_TEMPLATE)
        return self._jinja_template

    @property
    def single_transaction_url(self) -> str:
        """Single transaction url.

        Returns:
            str: A&AI bulk single transaction url.
        """
        return f"{self.url}/single-transaction"

    @property
    def failed_requests(self) -> List[AaiBulkRequest]:
        """Collection of failed requests.

        If user decide to retry bulk without failing request then they are
            stored in given collection for logging/debugging purposes.

        Returns:
            List[AaiBulkRequest]: List of failing bulk requests

        """
        if not self._failed_requests:
            return []
        return self._failed_requests

    def _add_failed_request(self, failed_request: AaiBulkRequest) -> None:
        """Add failed request into internal `failed_requests` collection.

        Args:
            failed_request (AaiBulkRequest): Request which failed

        """
        if not self._failed_requests:
            self._failed_requests = []
        self._failed_requests.append(failed_request)

    def _send_single_transaction_request(self,
                                         aai_requests: List[AaiBulkResponse]
                                         ) -> Iterable[AaiBulkResponse]:
        """Send single transaction request.

        Using send_message_json send chunk of requests to A&AI

        Args:
            aai_requests (List[AaiBulkResponse]): List of requests to be sent

        Yields:
            AaiBulkResponse: Response for each bulk request

        """
        if not aai_requests:
            self._logger.info("No operations to send, abort")
            return
        for response in self.send_message_json(
            "POST",
            "Send bulk A&AI request",
            self.single_transaction_url,
            data=self.jinja_template.render(operations=aai_requests)
        )["operation-responses"]:
            yield AaiBulkResponse(
                action=response["action"],
                uri=response["uri"],
                status_code=response["response-status-code"],
                body=response["response-body"]
            )

    def _get_failed_operation_index(self, failed_response_body: Optional[str]) -> int:
        """Get index of an operation which failed.

        Using regular expressions we are able to read an index of request which we sent
            and failed. Thanks to that we would be able to debug it, remove it and try to
            rerun whole bulk request.

        Args:
            failed_response_body (Optional[str]): Body of failed A&AI bulk request

        Returns:
            int: Index of a request which failed. -1 if regular expression didn't find
                any match

        """
        if not failed_response_body:
            return -1
        match: Match = self._operation_index_regex.match(failed_response_body)
        if not match:
            return -1
        groupsdict: Dict[str, Any] = match.groupdict()
        if groupsdict[self.FIRST_REGEX_GROUP_NAME]:
            str_index: str = groupsdict[self.FIRST_REGEX_GROUP_NAME]
        else:
            str_index = groupsdict[self.SECOND_REGEX_GROUP_NAME]
        return int(str_index)

    def _send_chunk(self, aai_requests: List[AaiBulkRequest],
                    remove_failed_operation_on_failure: bool = True) -> Iterable[AaiBulkResponse]:
        """Send a bulk requests chunk.

        If it failed and `remove_failed_operation_on_failure` is set
            then try to find which bulk request is failing, remove it and retry.

        Args:
            aai_requests (List[AaiBulkRequest]): List of requests to send
            remove_failed_operation_on_failure (bool, optional): Flag to determine if
                find failing request, remove it and retry. Defaults to True.

        Yields:
            AaiBulkResponse: Response for each bulk request

        """
        try:
            yield from self._send_single_transaction_request(aai_requests)
        except APIError as api_error:
            if not remove_failed_operation_on_failure:
                raise
            operation_index: int = self._get_failed_operation_index(api_error.response_text)
            if operation_index < 0:
                self._logger.error("Wanted to remove failing bulk operation, "
                                   "but there is no index on API response, "
                                   "probably it's an A&AI error!")
                raise
            self._add_failed_request(aai_requests.pop(operation_index))
            yield from self._send_chunk(aai_requests, remove_failed_operation_on_failure)

    def single_transaction(self,
                           aai_requests: Iterable[AaiBulkRequest],
                           remove_failed_operation_on_failure: bool = True
                           ) -> Iterable[AaiBulkResponse]:
        """Send aai requests using A&AI single transaction API.

        Args:
            aai_requests (List[AaiBulkRequest]): List of requests to send
            remove_failed_operation_on_failure (bool, optional): Flag to determine if
                find failing request, remove it and retry. Defaults to True.

        Yields:
            AaiBulkResponse: Response for each bulk request

        """
        for requests_chunk in chunked(aai_requests, self.chunk_size):
            yield from self._send_chunk(requests_chunk, remove_failed_operation_on_failure)
