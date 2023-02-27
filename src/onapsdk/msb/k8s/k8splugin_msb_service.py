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
from onapsdk.msb import MSB
from deprecated import deprecated


class K8sPluginViaMsb(MSB):
    """K8sPlugin via MSB base class."""

    base_url = f"{MSB.base_url}/api/multicloud-k8s/v1"
    api_version = "/v1"

    @classmethod
    @deprecated(version="11.0.0", reason="K8sPlugin should be used without MSB now")
    def base_url_and_version(cls):
        """Return base url with api version.

        Returns base url with api version
        """
        return f"{K8sPluginViaMsb.base_url}{K8sPluginViaMsb.api_version}"
