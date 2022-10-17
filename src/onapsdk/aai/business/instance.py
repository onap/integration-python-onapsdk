"""Base instance module."""
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

from ..aai_element import AaiResource


class Instance(AaiResource, ABC):
    """Abstract instance class."""

    def __init__(self,  # pylint: disable=too-many-arguments
                 resource_version: str = None,
                 model_invariant_id: str = None,
                 model_version_id: str = None) -> None:
        """Instance initialization.

        Args:
            resource_version (str, optional): Used for optimistic concurrency.
                Must be empty on create, valid on update and delete. Defaults to None.
            model_invariant_id (str, optional): The ASDC model id for this resource or
                service model. Defaults to None.
            model_version_id (str, optional): The ASDC model version for this resource or
                service model. Defaults to None.
        """
        super().__init__()
        self.resource_version: str = resource_version
        self.model_invariant_id: str = model_invariant_id
        self.model_version_id: str = model_version_id

    @abstractmethod
    def delete(self, a_la_carte: bool = True) -> "DeletionRequest":
        """Create instance deletion request.

        Send request to delete instance

        Args:
            a_la_carte (boolean): deletion mode

        Returns:
            DeletionRequest: Deletion request

        """
