"""SDC Element module."""
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
from abc import ABC, abstractmethod
from operator import itemgetter
from typing import Any, Dict, List, Optional

from onapsdk.sdc import SdcOnboardable
import onapsdk.constants as const


class SdcElement(SdcOnboardable, ABC):
    """Mother Class of all SDC elements."""

    ACTION_TEMPLATE = 'sdc_element_action.json.j2'
    ACTION_METHOD = 'PUT'

    def __init__(self, name: str = None) -> None:
        """Initialize the object."""
        super().__init__(name=name)
        self.human_readable_version: Optional[str] = None

    def _get_item_details(self) -> Dict[str, Any]:
        """
        Get item details.

        Returns:
            Dict[str, Any]: the description of the item

        """
        if self.created():
            url = f"{self._base_url()}/items/{self.identifier}/versions"
            results: Dict[str, Any] = self.send_message_json('GET', 'get item', url)
            if results["listCount"] > 1:
                items: List[Dict[str, Any]] = results["results"]
                return sorted(items, key=itemgetter("creationTime"), reverse=True)[0]
            return results["results"][0]
        return {}

    def load(self) -> None:
        """Load Object information from SDC."""
        vsp_details = self._get_item_details()
        if vsp_details:
            self._logger.debug("details found, updating")
            self.version = vsp_details['id']
            self.human_readable_version = vsp_details["name"]
            self.update_informations_from_sdc(vsp_details)
        else:
            # exists() method check if exists AND update identifier
            self.exists()

    def update_informations_from_sdc(self, details: Dict[str, Any]) -> None:
        """

        Update instance with details from SDC.

        Args:
            details ([type]): [description]

        """
    def update_informations_from_sdc_creation(self,
                                              details: Dict[str, Any]) -> None:
        """

        Update instance with details from SDC after creation.

        Args:
            details ([type]): the details from SDC

        """
    @classmethod
    def _base_url(cls) -> str:
        """
        Give back the base url of Sdc.

        Returns:
            str: the base url

        """
        return f"{cls.base_front_url}/sdc1/feProxy/onboarding-api/v1.0"

    @classmethod
    def _base_create_url(cls) -> str:
        """
        Give back the base url of Sdc.

        Returns:
            str: the base url

        """
        return f"{cls.base_front_url}/sdc1/feProxy/onboarding-api/v1.0"

    def _generate_action_subpath(self, action: str) -> str:
        """

        Generate subpath part of SDC action url.

        Args:
            action (str): the action that will be done

        Returns:
            str: the subpath part

        """
        subpath = self._sdc_path()
        if action in (const.COMMIT, const.ARCHIVE):
            subpath = "items"
        return subpath

    def _version_path(self) -> str:
        """
        Give the end of the path for a version.

        Returns:
            str: the end of the path

        """
        return f"{self.identifier}/versions/{self.version}"

    def _action_url(self, base: str, subpath: str, version_path: str,
                    action_type: str = None) -> str:
        """
        Generate action URL for SDC.

        Args:
            base (str): base part of url
            subpath (str): subpath of url
            version_path (str): version path of the url
            action_type (str, optional): the type of action. UNUSED here

        Returns:
            str: the URL to use

        """
        if action_type == const.ARCHIVE:
            version_path = version_path.split("/", maxsplit=1)[0]
        return f"{base}/{subpath}/{version_path}/actions"

    @classmethod
    def _get_objects_list(cls, result: List[Dict[str, Any]]
                          ) -> List[Dict[str, Any]]:
        """
        Import objects created in SDC.

        Args:
            result (Dict[str, Any]): the result returned by SDC in a Dict

        Return:
            List[Dict[str, Any]]: the list of objects

        """
        return result['results']

    @classmethod
    def _get_all_url(cls) -> str:
        """
        Get URL for all elements in SDC.

        Returns:
            str: the url

        """
        return f"{cls._base_url()}/{cls._sdc_path()}"

    @property
    def delete_url(self) -> str:
        """Get an url to delete element.

        Returns:
            str: Url which can be used to delete SDC element

        """
        return f"{self._base_url()}/{self._sdc_path()}/{self.identifier}"

    def _copy_object(self, obj: 'SdcElement') -> None:
        """
        Copy relevant properties from object.

        Args:
            obj (SdcElement): the object to "copy"

        """
        self.identifier = obj.identifier

    def _get_version_from_sdc(self, sdc_infos: Dict[str, Any]) -> str:
        """
        Get version from SDC results.

        Args:
            sdc_infos (Dict[str, Any]): the result dict from SDC

        Returns:
            str: the version

        """
        return sdc_infos['version']['id']

    def _get_identifier_from_sdc(self, sdc_infos: Dict[str, Any]) -> str:
        """
        Get identifier from SDC results.

        Args:
            sdc_infos (Dict[str, Any]): the result dict from SDC

        Returns:
            str: the identifier

        """
        return sdc_infos['itemId']

    @classmethod
    @abstractmethod
    def import_from_sdc(cls, values: Dict[str, Any]) -> 'SdcElement':
        """
        Import SdcElement from SDC.

        Args:
            values (Dict[str, Any]): dict to parse returned from SDC.

        Raises:
            NotImplementedError: this is an abstract method.

        """
        raise NotImplementedError("SdcElement is an abstract class")

    def delete(self) -> None:
        """Delete SDC element.

        Send a request to SDC to delete that element.

        """
        self.send_message(
            "DELETE",
            "Delete SDC element",
            self.delete_url
        )
