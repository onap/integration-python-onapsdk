"""Query module."""
#   Copyright 2023 Deutsche Telekom AG
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


@dataclass
class GVK:
    """Class to store GVK info of k8s resource.

    Contains group, version, and kind information
    """

    def __init__(self, gvk: dict) -> None:
        """Gvk object initialization.

        Args:
            Group (str): Group of resource
            Version (str): Version of resource
            Kind (str): Kind name
        """
        super().__init__()
        self.group: str = gvk["Group"]
        self.version: str = gvk["Version"]
        self.kind: str = gvk["Kind"]

    @classmethod
    def to_list_of_gvk(cls, gvk_list: list) -> list:
        """Convert list of dicts to list of GVK.

        Args:
            gvk_list (list): list of gvk dicts

        Returns:
            Converted list

        """
        final_list = []
        if gvk_list is not None:
            for gvk in gvk_list:
                final_list.append(cls(gvk))
        return final_list


@dataclass
class ResourceStatus:
    """Class to store status of singular k8s resource."""

    def __init__(self, status: dict) -> None:
        """Status object initialization.

        Args:
            GVK (str): GVK of resource
            name (str): name of resource
            status (str): full status of resource
        """
        super().__init__()
        self.name: str = status["name"]
        self.gvk: GVK = GVK(status["GVK"])
        self.status: dict = status["status"]