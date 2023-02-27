"""Definition module."""
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

# pylint: disable=too-many-arguments, too-few-public-methods, too-many-ancestors, useless-super-delegation, duplicate-code
@dataclass
@deprecated(version="11.0.0", reason="K8sPlugin should be used without MSB now")
class Profile(K8sPluginViaMsb, onapsdk.k8s.Profile):
    """Profile class via MSB."""

    def __init__(self, rb_name: str,
                 rb_version: str,
                 profile_name: str,
                 namespace: str,
                 kubernetes_version: str,
                 labels: dict = None,
                 release_name: str = None,
                 extra_resource_types: list = None) -> None:
        """Profile object initialization.

        Args:
            rb_name (str): Definition name
            rb_version (str): Definition version
            profile_name (str): Name of profile
            release_name (str): Release name, if release_name is not provided,
            namespace (str): Namespace that service is created in
            kubernetes_version (str): Required Kubernetes version
            labels (dict): Extra Labels for k8s resources
            extra_resource_types (list): Extra k8s resources types (GVK) for status monitoring
        """
        super().__init__(rb_name, rb_version, profile_name, namespace, kubernetes_version,
                         labels, release_name, extra_resource_types)


# pylint: disable=too-many-arguments, too-few-public-methods, too-many-ancestors, useless-super-delegation, duplicate-code
@dataclass
@deprecated(version="11.0.0", reason="K8sPlugin should be used without MSB now")
class ConfigurationTemplate(K8sPluginViaMsb, onapsdk.k8s.ConfigurationTemplate):
    """ConfigurationTemplate class via MSB."""

    def __init__(self, rb_name: str,
                 rb_version: str,
                 template_name: str,
                 description: str,
                 chart_name="",
                 has_content=False) -> None:
        """Configuration-Template object initialization.

        Args:
            rb_name (str): Definition name
            rb_version (str): Definition version
            template_name (str): Configuration template name
            description (str): Namespace that service is created in
            chart_name (str): Name of the charft of uploaded content
            has_content (bool): If false cotent is taken fro mthe main definition
        """
        super().__init__(rb_name, rb_version, template_name, description, chart_name, has_content)


# pylint: disable=too-many-arguments, too-few-public-methods, too-many-ancestors, useless-super-delegation, duplicate-code
@dataclass
@deprecated(version="11.0.0", reason="K8sPlugin should be used without MSB now")
class Definition(K8sPluginViaMsb, onapsdk.k8s.Definition):
    """Definition class via MSB."""

    profile_class = Profile
    config_template_class = ConfigurationTemplate

    def __init__(self, rb_name: str,
                 rb_version: str,
                 chart_name: str,
                 description: str,
                 labels: dict) -> None:
        """Definition object initialization.

        Args:
            rb_name (str): Definition name
            rb_version (str): Definition version
            chart_name (str): Chart name, optional field, will be detected if it is not provided
            description (str): Definition description
            labels (str): Labels
        """
        super().__init__(rb_name, rb_version, chart_name, description, labels)
