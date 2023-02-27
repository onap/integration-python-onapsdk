"""Instantiation module."""
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
class InstantiationRequest(onapsdk.k8s.InstantiationRequest):
    """Instantiation Request class via MSB."""

    def __init__(self, request: dict) -> None:
        """Request object initialization.

        Args:
            cloud_region_id (str): Cloud region ID
            profile_name (str): Name of profile
            rb_name (str): Definition name
            rb_version (str): Definition version
            override_values (dict): Optional parameters
            labels (dict): Optional labels
        """
        super().__init__(request)


@dataclass
@deprecated(version="11.0.0", reason="K8sPlugin should be used without MSB now")
class InstantiationParameter(onapsdk.k8s.InstantiationParameter):
    """Class to store instantiation parameters used to pass override_values and labels.

    Contains two values: name of parameter and it's value
    """


# pylint: disable=too-many-ancestors, useless-super-delegation, duplicate-code
@dataclass
@deprecated(version="11.0.0", reason="K8sPlugin should be used without MSB now")
class Configuration(K8sPluginViaMsb, onapsdk.k8s.Configuration):
    """Configuration class."""

    def __init__(self, instance_id: str,
                 config_name: str,
                 template_name: str,
                 description: str,
                 config_version: str,
                 config_tag: str) -> None:
        """Initialize Configuration object.

        Args:
            instance_id (str): instance ID
            config_name (str): Name of the configuration
            template_name (str): Name of the template
            description (str): Description
            config_version (str): Config version
            config_tag (str): Config tag
        """
        super().__init__(instance_id, config_name, template_name, description,
                         config_version, config_tag)


# pylint: disable=too-many-ancestors, useless-super-delegation, duplicate-code
@dataclass
@deprecated(version="11.0.0", reason="K8sPlugin should be used without MSB now")
class Instance(K8sPluginViaMsb, onapsdk.k8s.Instance):
    """Instance class via MSB."""

    config_class = Configuration

    def __init__(self, instance_id: str,
                 namespace: str,
                 request: InstantiationRequest,
                 resources: dict = None,
                 override_values: dict = None) -> None:
        """Instance object initialization.

        Args:
            instance_id (str): instance ID
            namespace (str): namespace that instance is created in
            request (InstantiationRequest): datails of the instantiation request
            resources (dict): Created resources
            override_values (dict): Optional values
        """
        super().__init__(instance_id, namespace, request, resources, override_values)
