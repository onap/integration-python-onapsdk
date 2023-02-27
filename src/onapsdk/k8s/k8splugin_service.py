"""K8s package."""
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
from typing import Any, Dict

from onapsdk.configuration import settings
from onapsdk.onap_service import OnapService


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


class K8sPlugin(OnapService):
    """K8sPlugin base class."""

    base_url = settings.K8SPLUGIN_URL
    api_version = "/v1"
    headers = OnapService.headers

    @classmethod
    def base_url_and_version(cls):
        """Return base url with api version.

        Returns base url with api version
        """
        return f"{K8sPlugin.base_url}{K8sPlugin.api_version}"

    def query_resource_status(self,
                              query_url: str,
                              namespace: str = None,
                              name: str = None,
                              labels: dict = None) -> Dict[str, Any]:
        """Call a query request.

        Args:
            query_url (str): A query base url
            namespace (str): Namespace of k8s resource
            name (str): Name of k8s resource
            labels (dict): Lables of k8s resource

        Returns:
            Query request response dictionary

        """
        if name is not None:
            query_url = f"{query_url}&Name={name}"
        if namespace is not None:
            query_url = f"{query_url}&Namespace={namespace}"
        if labels is not None and len(labels) > 0:
            query_url = f"{query_url}&Labels="
            for label_name, label_value in labels.items():
                query_url = f"{query_url}{label_name}%3D{label_value},"
            query_url = query_url.rstrip(',')

        return self.send_message_json(
            "GET",
            "Query region status",
            query_url
        )


class RemovableK8sPlugin(K8sPlugin):
    """K8S plugin resource which could be removed."""

    @property
    def url(self) -> str:
        """Object url.

        Returns:
            str: Object's url

        """
        raise NotImplementedError

    def delete(self) -> None:
        """Delete k8s plugin object."""
        self.send_message(
            "DELETE",
            f"Delete {self.__class__.__name__}",
            self.url
        )
