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
from .definition import Definition, Profile, ConfigurationTemplate
from .connectivity_info import ConnectivityInfo
from .instance import InstantiationParameter, InstantiationRequest, Instance
from .instance import InstanceStatus, Configuration, ConfigurationTag
from .k8splugin_service import K8sPlugin, GVK, ResourceStatus
from .region import CloudRegionStatus, CloudRegion
