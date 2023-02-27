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
from dataclasses import dataclass
import onapsdk.k8s
from deprecated import deprecated
from .k8splugin_msb_service import K8sPluginViaMsb


# pylint: disable=too-many-ancestors, useless-super-delegation, duplicate-code
@dataclass
@deprecated(version="11.0.0", reason="K8sPlugin should be used without MSB now")
class ConnectivityInfo(K8sPluginViaMsb, onapsdk.k8s.ConnectivityInfo):
    """Connectivity-Info via MSB class."""

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
        super().__init__(cloud_region_id, cloud_owner, other_connectivity_list, kubeconfig)
