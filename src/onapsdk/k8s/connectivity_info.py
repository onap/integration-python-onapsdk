"""Connectivity-Info module."""
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
from onapsdk.utils.jinja import jinja_env
from .k8splugin_service import RemovableK8sPlugin


class ConnectivityInfo(RemovableK8sPlugin):
    """Connectivity-Info class."""

    def __init__(self, cloud_region_id: str,
                 cloud_owner: str,
                 other_connectivity_list: dict,
                 kubeconfig: str) -> None:
        """Connectivity-info object initialization.

        Args:
            cloud_region_id (str): Cloud region ID
            cloud_owner (str): Cloud owner name
            other_connectivity_list (dict): Optional other connectivity list
            kubeconfig (str): kubernetes cluster kubeconfig
        """
        super().__init__()
        self.cloud_region_id: str = cloud_region_id
        self.cloud_owner: str = cloud_owner
        self.other_connectivity_list: dict = other_connectivity_list
        self.kubeconfig: str = kubeconfig

    @property
    def url(self) -> str:
        """URL address for Definition Based calls.

        Returns:
            str: URL to RB Definition

        """
        return f"{self.base_url_and_version()}/connectivity-info/{self.cloud_region_id}"

    @classmethod
    def get_connectivity_info_by_region_id(cls, cloud_region_id: str) -> "ConnectivityInfo":
        """Get connectivity-info by its name (cloud region id).

        Args:
            cloud_region_id (str): Cloud region ID

        Returns:
            ConnectivityInfo: Connectivity-Info object

        """
        url: str = f"{cls.base_url_and_version()}/connectivity-info/{cloud_region_id}"
        connectivity_info: dict = cls.send_message_json(
            "GET",
            "Get Connectivity Info",
            url
        )
        return cls(
            connectivity_info["cloud-region"],
            connectivity_info["cloud-owner"],
            connectivity_info.get("other-connectivity-list"),
            connectivity_info["kubeconfig"]
        )

    @classmethod
    def create(cls,
               cloud_region_id: str,
               cloud_owner: str,
               kubeconfig: bytes = None) -> "ConnectivityInfo":
        """Create Connectivity Info.

        Args:
            cloud_region_id (str): Cloud region ID
            cloud_owner (str): Cloud owner name
            kubeconfig (bytes): kubernetes cluster kubeconfig file

        Returns:
            ConnectivityInfo: Created object

        """
        json_file = jinja_env().get_template("multicloud_k8s_add_connectivity_info.json.j2").render(
            cloud_region_id=cloud_region_id,
            cloud_owner=cloud_owner
        )
        url: str = f"{cls.base_url_and_version()}/connectivity-info"
        cls.send_message(
            "POST",
            "Create Connectivity Info",
            url,
            files={"file": kubeconfig,
                   "metadata": (None, json_file)},
            headers={}
        )
        return cls.get_connectivity_info_by_region_id(cloud_region_id)
