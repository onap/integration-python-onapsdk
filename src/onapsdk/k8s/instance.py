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
import json
from typing import Any, Dict, Iterator
from dataclasses import dataclass

from onapsdk.utils.jinja import jinja_env
from .k8splugin_service import QueryResourceStatusMixin, ResourceStatus, RemovableK8sPlugin


# pylint: disable=too-many-arguments
@dataclass
class InstantiationRequest:
    """Instantiation Request class."""

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
        super().__init__()
        self.cloud_region_id: str = request["cloud-region"]
        self.profile_name: str = request["profile-name"]
        self.rb_name: str = request["rb-name"]
        self.rb_version: str = request["rb-version"]
        self.override_values: dict = request["override-values"]
        self.labels: dict = request["labels"]


@dataclass
class InstantiationParameter:
    """Class to store instantiation parameters used to pass override_values and labels.

    Contains two values: name of parameter and it's value
    """

    name: str
    value: str


class InstanceBase(RemovableK8sPlugin):
    """InstanceBase class."""

    def __init__(self, instance_id: str) -> None:
        """Instance-Base object initialization.

        Args:
            instance_id (str): instance ID
        """
        super().__init__()
        self.instance_id: str = instance_id

    @property
    def url(self) -> str:
        """URL address.

        Returns:
            str: URL to Instance

        """
        return f"{self.base_url_and_version()}/instance/{self.instance_id}"


@dataclass
class ConfigurationTag:
    """Class to store configuration tag information.

    Contains two values: name of tag and version of associated configuration
    """

    config_tag: str
    config_version: str


class Configuration(InstanceBase):
    """Configuration class."""

    def __init__(self, instance_id: str,
                 config_name: str,
                 template_name: str,
                 description: str,
                 config_version: str,
                 config_tag: str,
                 values: dict = None) -> None:
        """Initialize Configuration object.

        Args:
            instance_id (str): instance ID
            config_name (str): Name of the configuration
            template_name (str): Name of the template
            description (str): Description
            config_version (str): Config version
            config_tag (str): Config tag
            values (dict): Overrides values used to create configuration
        """
        super().__init__(instance_id)
        self.name = config_name
        self.template_name = template_name
        self.config_version = str(config_version)
        self.config_tag = config_tag
        self.description = description
        self.values = values

    @property
    def url(self) -> str:
        """URL address for Configuration calls.

        Returns:
            str: URL to Configuration

        """
        return f"{self.base_url_and_version()}/instance/{self.instance_id}/config/{self.name}"

    def rollback_to(self, config_version: str, config_tag: str) -> None:
        """Rollback configuration to specific version.

        Args:
            config_version (str): version of configuration
            config_tag (str): tag of configuration

        """
        url: str = f"{self.url}/rollback"

        params = {}
        if config_version is not None:
            params["config-version"] = config_version
        if config_tag is not None:
            params["config-tag"] = config_tag
        self.send_message_json(
            "POST",
            "Rollback Configuration",
            url,
            data=json.dumps(params),
            headers={}
        )
        self.config_version = config_version
        self.config_tag = config_tag

    def update(self, override_values: dict) -> "Configuration":
        """Update configuration.

        Args:
            override_values (dict): Override values

        Returns:
            Configuration: Updated object

        """
        body = json.dumps(override_values)

        config: dict = self.send_message_json(
            "PUT",
            "Update configuration",
            self.url,
            data=jinja_env().get_template("multicloud_k8s_create_configuration_for_"
                                          "instance.json.j2").render(
                                              config_name=self.name,
                                              template_name=self.template_name,
                                              description=self.description,
                                              override_values=body
                                          )
        )
        return self.get_config_by_version(str(config["config-version"]))

    def tag_config_version(self, config_tag: str) -> None:
        """Tag configuration.

        Args:
            config_tag (str): Tag name of the configuration version

        """
        body = json.dumps({"tag-name": config_tag})

        self.send_message(
            "POST",
            "Tag configuration",
            f"{self.url}/tagit",
            data=body
        )

    def get_config_by_version(self, config_version: str) -> "Configuration":
        """Get configuration by version.

        Args:
            config_version (str): Config version

        Returns:
            Configuration: object

        """
        config: dict = self.send_message_json(
            "GET",
            "Get Configuration by version",
            f"{self.url}/version/{config_version}"
        )
        return self.__class__(
            self.instance_id,
            self.name,
            config["template-name"],
            config["description"],
            config["config-version"],
            config["config-tag"],
            config["values"]
        )

    def get_config_versions(self) -> Iterator["Configuration"]:
        """Get List of configuration versions.

        Returns:
            List of versions for configuration

        """
        for config in self.send_message_json("GET",
                                             "Get config versions",
                                             f"{self.url}/version"):
            yield self.__class__(
                self.instance_id,
                self.name,
                config["template-name"],
                config["description"],
                config["config-version"],
                config["config-tag"],
                config["values"]
            )

    def get_config_by_tag(self, config_tag: str) -> "Configuration":
        """Get configuration by tag.

        Args:
            config_tag (str): Name of tag

        Returns:
            Configuration: object

        """
        config: dict = self.send_message_json(
            "GET",
            "Get Configuration by tag",
            f"{self.url}/tag/{config_tag}"
        )
        return self.__class__(
            self.instance_id,
            self.name,
            config["template-name"],
            config["description"],
            config["config-version"],
            config["config-tag"],
            config["values"]
        )

    def get_config_tags(self) -> Iterator["ConfigurationTag"]:
        """Get List of Tags.

        Returns:
            List of tags for configuration

        """
        for tag in self.send_message_json("GET",
                                          "Get config tags",
                                          f"{self.url}/tag"):
            yield ConfigurationTag(
                config_tag=tag["config-tag"],
                config_version=str(tag["config-version"])
            )

    def create_delete_version(self) -> "Configuration":
        """Create delete version of configuration."""
        url: str = f"{self.url}/delete"

        config: dict = self.send_message_json(
            "POST",
            "Delete Resources Configuration",
            url
        )
        return self.__class__(
            self.instance_id,
            self.name,
            config["template-name"],
            config["description"],
            config["config-version"],
            config["config-tag"],
            config["values"]
        )

    def delete_without_resources(self) -> None:
        """Delete Instance Based object."""
        self.send_message(
            "DELETE",
            f"Delete {self.__class__.__name__}",
            f"{self.url}?deleteConfigOnly=true"
        )


@dataclass
class InstanceStatus:
    """Class to store status of the Instance."""

    instance_id: str
    request: InstantiationRequest
    resource_count: str
    ready: bool
    resources_status: list


class Instance(InstanceBase, QueryResourceStatusMixin):
    """Instance class."""

    config_class = Configuration
    request_class = InstantiationRequest

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
        super().__init__(instance_id)
        self.namespace: str = namespace
        self.request: InstantiationRequest = request
        self.resources: dict = resources
        self.override_values: dict = override_values

    @classmethod
    def get_all(cls) -> Iterator["Instance"]:
        """Get all instantiated Kubernetes resources.

        Yields:
            Instantiation: Instantiation object

        """
        for resource in cls.send_message_json("GET",
                                              "Get Kubernetes resources",
                                              f"{cls.base_url_and_version()}/instance"):
            yield cls(
                instance_id=resource["id"],
                namespace=resource["namespace"],
                request=cls.request_class(resource["request"])
            )

    @classmethod
    def get_by_id(cls, instance_id: str) -> "Instance":
        """Get Kubernetes resource by id.

        Args:
            instance_id (str): instance ID

        Returns:
            Instantiation: Instantiation object

        """
        url: str = f"{cls.base_url_and_version()}/instance/{instance_id}"
        resource: dict = cls.send_message_json(
            "GET",
            "Get Kubernetes resource by id",
            url
        )
        return cls(
            instance_id=resource["id"],
            namespace=resource["namespace"],
            request=cls.request_class(resource["request"]),
            resources=resource["resources"],
            override_values=resource.get("override-values")
        )

    @classmethod
    def create(cls,
               cloud_region_id: str,
               profile_name: str,
               rb_name: str,
               rb_version: str,
               override_values: dict = None,
               labels: dict = None) -> "Instance":
        """Create Instance.

        Args:
            cloud_region_id (str): Cloud region ID
            profile_name (str): Name of profile to be instantiated
            rb_name: (bytes): Definition name
            rb_version (str): Definition version
            override_values (dict): List of optional override values
            labels (dict): List of optional labels

        Returns:
            Instance: Created object

        """
        if labels is None:
            labels = {}
        if override_values is None:
            override_values = {}
        url: str = f"{cls.base_url_and_version()}/instance"
        response: dict = cls.send_message_json(
            "POST",
            "Create Instance",
            url,
            data=jinja_env().get_template("multicloud_k8s_instantiate.json.j2").render(
                cloud_region_id=cloud_region_id,
                profile_name=profile_name,
                rb_name=rb_name,
                rb_version=rb_version,
                override_values=override_values,
                labels=labels),
            headers={}
        )
        return cls(
            instance_id=response["id"],
            namespace=response["namespace"],
            request=cls.request_class(response["request"]),
            resources=response["resources"],
            override_values=response.get("override-values")
        )

    def upgrade(self,
                cloud_region_id: str,
                profile_name: str,
                rb_name: str,
                rb_version: str,
                override_values: dict = None,
                labels: dict = None) -> "Instance":
        """Upgrade Instance.

        Args:
            cloud_region_id (str): Cloud region ID
            profile_name (str): Name of profile to be instantiated
            rb_name: (bytes): Definition name
            rb_version (str): Definition version
            override_values (dict): List of optional override values
            labels (dict): List of optional labels

        Returns:
            Instance: Created object

        """
        if labels is None:
            labels = {}
        if override_values is None:
            override_values = {}
        url: str = f"{self.url}/upgrade"
        response: dict = self.send_message_json(
            "POST",
            "Upgrade Instance",
            url,
            data=jinja_env().get_template("multicloud_k8s_instantiate.json.j2").render(
                cloud_region_id=cloud_region_id,
                profile_name=profile_name,
                rb_name=rb_name,
                rb_version=rb_version,
                override_values=override_values,
                labels=labels),
            headers={}
        )
        return self.__class__(
            instance_id=response["id"],
            namespace=response["namespace"],
            request=self.request_class(response["request"]),
            resources=response["resources"],
            override_values=response.get("override-values")
        )

    def create_configuration(self, config_name: str,
                             template_name: str,
                             override_values: dict = None,
                             description="") -> "Configuration":
        """Create configuration instance.

        Args:
            config_name (str): Name of the configuration
            template_name (str): Name of the template
            description (str): Description
            override_values (dict): Override values

        Returns:
            Configuration: Created object

        """
        url: str = f"{self.url}/config"

        body = json.dumps(override_values)

        self.send_message(
            "POST",
            "Create configuration",
            url,
            data=jinja_env().get_template("multicloud_k8s_create_configuration_for_"
                                          "instance.json.j2").render(
                                              config_name=config_name,
                                              template_name=template_name,
                                              description=description,
                                              override_values=body
                                          )
        )

        return self.get_configuration_by_name(config_name)

    def get_all_configurations(self) -> Iterator["Configuration"]:
        """Get List of configurations.

        Returns:
            List of configurations

        """
        for config in self.send_message_json("GET",
                                             "Get all configurations",
                                             f"{self.url}/config"):
            yield self.config_class(
                self.instance_id,
                config["config-name"],
                config["template-name"],
                config["description"],
                config["config-version"],
                config["config-tag"],
                config["values"]
            )

    def get_configuration_by_name(self, config_name: str) -> "Configuration":
        """Get configuration.

        Args:
            config_name (str): Name of the configuration

        Returns:
            Configuration: object

        """
        url: str = f"{self.url}/config/{config_name}"

        config: dict = self.send_message_json(
            "GET",
            "Get Configuration by name",
            url
        )
        return self.config_class(
            self.instance_id,
            config_name,
            config["template-name"],
            config["description"],
            config["config-version"],
            config["config-tag"],
            config["values"]
        )

    def get_status(self) -> "InstanceStatus":
        """Get instance status.

        Returns:
            Status of the instance

        """
        status: dict = self.send_message_json(
            "GET",
            "Get status",
            f"{self.url}/status"
        )
        resources_status = []
        for res_status in status["resourcesStatus"]:
            resources_status.append(ResourceStatus(res_status))
        return InstanceStatus(
            self.instance_id,
            request=self.request_class(status["request"]),
            resource_count=int(status["resourceCount"]),
            ready=bool(status["ready"]),
            resources_status=resources_status
        )

    def query_status(self,
                     kind: str,
                     api_version: str,
                     name: str = None,
                     labels: dict = None) -> "InstanceStatus":
        """Query instance status.

        Args:
            kind (str): Kind of k8s resource
            api_version (str): Api version of k8s resource
            name (str): Name of k8s resource
            labels (dict): Lables of k8s resource

        Returns:
            Filtered status of the instance

        """
        url = f"{self.url}/query"
        status: Dict[Any] = self.query_resource_status(url,
                                                       api_version=api_version,
                                                       kind=kind,
                                                       name=name,
                                                       labels=labels)
        return InstanceStatus(
            self.instance_id,
            request=self.request_class(status["request"]),
            resource_count=int(status["resourceCount"]),
            ready=bool(status["ready"]),
            resources_status=[ResourceStatus(res_status) for
                              res_status in status["resourcesStatus"]]
        )
