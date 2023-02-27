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
from .k8splugin_service import K8sPlugin
from .connectivity_info import ConnectivityInfo


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


@dataclass
class CloudRegionStatus:
    """Class to store status of the Region."""

    resource_count: str
    resources_status: list


# pylint: disable=too-many-arguments
@dataclass
class CloudRegion(K8sPlugin):
    """Cloud region information."""

    def __init__(self,
                 cloud_region_id: str,
                 info: ConnectivityInfo) -> None:
        """Region object initialization.

        Args:
            cloud_region_id (str): Cloud region ID
            info (ConnectivityInfo): Connectivity Info

        """
        super().__init__()
        self.cloud_region_id = cloud_region_id
        self.connectivity_info = info

    @classmethod
    def create(cls,
               cloud_region_id: str,
               cloud_owner: str = None,
               kubeconfig: bytes = None) -> "CloudRegion":
        """Create Cloud Region.

        Args:
            cloud_region_id (str): Cloud region ID
            cloud_owner (str): Cloud owner name
            kubeconfig (str): kubernetes cluster kubeconfig

        Returns:
            CloudRegion: Created region object

        """
        if cloud_owner is None:
            cloud_owner = cloud_region_id
        info = ConnectivityInfo.create(cloud_region_id, cloud_owner, kubeconfig)
        return CloudRegion(cloud_region_id, info)

    def delete(self) -> None:
        """Delete Region and associated Connectivity Information."""
        self.connectivity_info.delete()

    @classmethod
    def get_by_region_id(cls, cloud_region_id: str) -> "CloudRegion":
        """Get Region Information."""
        info = ConnectivityInfo.get_connectivity_info_by_region_id(cloud_region_id)
        return CloudRegion(cloud_region_id, info)

    def query_resources(self,
                        kind: str,
                        api_version: str,
                        namespace: str = None,
                        name: str = None,
                        labels: dict = None) -> "CloudRegionStatus":
        """Query for resources in the cloud region.

        Args:
            kind (str): Kind of k8s resource
            api_version (str): Api version of k8s resource
            namespace (str): Namespace of k8s resource
            name (str): Name of k8s resource
            labels (dict): Lables of k8s resource

        Returns:
            Filtered status of the cloud region

        """
        url = f"{self.base_url_and_version()}/query?CloudRegion={self.cloud_region_id}"\
              f"&ApiVersion={api_version}&Kind={kind}"
        if name is not None:
            url = f"{url}&Name={name}"
        if namespace is not None:
            url = f"{url}&Namespace={namespace}"
        if labels is not None and len(labels) > 0:
            url = f"{url}&Labels="
            for label_name, label_value in labels:
                url = f"{url}{label_name}%3D{label_value},"
            url = url.rstrip(',')

        status: dict = self.send_message_json(
            "GET",
            "Query region status",
            url
        )
        resources_status = []
        for res_status in status["resourcesStatus"]:
            resources_status.append(ResourceStatus(res_status))
        return CloudRegionStatus(
            resource_count=int(status["resourceCount"]),
            resources_status=resources_status
        )
