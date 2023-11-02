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
from typing import Iterator
from dataclasses import dataclass
from onapsdk.utils.jinja import jinja_env
from .k8splugin_service import GVK, RemovableK8sPlugin


# pylint: disable=too-many-arguments, too-few-public-methods
class DefinitionBase(RemovableK8sPlugin):
    """DefinitionBase class."""

    def __init__(self, rb_name: str,
                 rb_version: str) -> None:
        """Definition-Base object initialization.

        Args:
            rb_name (str): Definition name
            rb_version (str): Definition version
        """
        super().__init__()
        self.rb_name: str = rb_name
        self.rb_version: str = rb_version

    @property
    def url(self) -> str:
        """URL address for Definition Based calls.

        Returns:
            str: URL to RB Definition

        """
        return f"{self.base_url_and_version()}/rb/definition/{self.rb_name}/{self.rb_version}"

    def upload_artifact(self, package: bytes = None):
        """Upload artifact.

        Args:
            package (bytes): Artifact to be uploaded to multicloud-k8s plugin

        """
        url: str = f"{self.url}/content"
        self.send_message(
            "POST",
            "Upload Artifact content",
            url,
            data=package,
            headers={}
        )


@dataclass
class Profile(DefinitionBase):
    """Profile class."""

    def __init__(self, rb_name: str,
                 rb_version: str,
                 profile_name: str,
                 namespace: str,
                 kubernetes_version: str,
                 labels: dict = None,
                 release_name: str = None,
                 extra_resource_types: dict = None) -> None:
        """Profile object initialization.

        Args:
            rb_name (str): Definition name
            rb_version (str): Definition version
            profile_name (str): Name of profile
            release_name (str): Release name, if release_name is not provided,
            namespace (str): Namespace that service is created in
            kubernetes_version (str): Required Kubernetes version
            labels (dict): Extra Labels for k8s resources
            extra_resource_types (dict): Extra k8s resources types (GVK) for status monitoring
        """
        super().__init__(rb_name, rb_version)
        self.profile_name: str = profile_name
        if release_name is None:
            release_name = profile_name
        self.release_name: str = release_name
        self.namespace: str = namespace
        self.kubernetes_version: str = kubernetes_version
        self.labels: dict = labels
        if self.labels is None:
            self.labels = {}
        self.extra_resource_types: dict = extra_resource_types
        if self.extra_resource_types is None:
            self.extra_resource_types = {}

    @property
    def url(self) -> str:
        """URL address for Profile calls.

        Returns:
            str: URL to RB Profile

        """
        return f"{self.base_url_and_version()}/rb/definition/{self.rb_name}/{self.rb_version}"\
               f"/profile/{self.profile_name}"

    def update(self) -> "Profile":
        """Update Profile for Definition.

        Returns:
            Profile: Updated object

        """
        profile: dict = self.send_message_json(
            "PUT",
            "Update profile for definition",
            self.url,
            data=jinja_env().get_template("multicloud_k8s_create_profile_"
                                          "for_definition.json.j2").render(
                                              rb_name=self.rb_name,
                                              rb_version=self.rb_version,
                                              profile_name=self.profile_name,
                                              release_name=self.release_name,
                                              namespace=self.namespace,
                                              kubernetes_version=self.kubernetes_version,
                                              labels=self.labels,
                                              extra_types=self.extra_resource_types
                                          )
        )
        return self.__class__(
            self.rb_name,
            self.rb_version,
            profile["profile-name"],
            profile["namespace"],
            profile.get("kubernetes-version"),
            profile.get("labels"),
            profile.get("release-name")
        )


@dataclass
class ConfigurationTemplate(DefinitionBase):
    """ConfigurationTemplate class."""

    @property
    def url(self) -> str:
        """URL address for ConfigurationTemplate calls.

        Returns:
            str: URL to Configuration template in Multicloud-k8s API.

        """
        return f"{self.base_url_and_version()}/rb/definition/{self.rb_name}/{self.rb_version}"\
               f"/config-template/{self.template_name}"

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
        super().__init__(rb_name, rb_version)
        self.template_name: str = template_name
        self.description: str = description
        self.chart_name: str = chart_name
        self.has_content: bool = has_content

    def update(self) -> "ConfigurationTemplate":
        """Update Configuration Template for Definition.

        Returns:
            ConfigurationTemplate: Updated object

        """
        template: dict = self.send_message_json(
            "PUT",
            "Update config template for definition",
            self.url,
            data=jinja_env().get_template("multicloud_k8s_create_configuration_"
                                          "template.json.j2").render(
                                              template_name=self.template_name,
                                              description=self.description
                                          )
        )
        return self.__class__(
            self.rb_name,
            self.rb_version,
            template["template-name"],
            template.get("description"),
            template.get("chart-name"),
            template.get("has-content")
        )


@dataclass
class Definition(DefinitionBase):
    """Definition class."""

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
        super().__init__(rb_name, rb_version)
        self.chart_name: str = chart_name
        self.description: str = description
        self.labels: dict = labels

    @classmethod
    def get_all(cls):
        """Get all definitions.

        Yields:
            Definition: Definition object

        """
        for definition in cls.send_message_json("GET",
                                                "Get definitions",
                                                f"{cls.base_url_and_version()}/rb/definition"):
            yield cls(
                definition["rb-name"],
                definition["rb-version"],
                definition.get("chart-name"),
                definition.get("description"),
                definition.get("labels")
            )

    @classmethod
    def get_definition_by_name_version(cls, rb_name: str, rb_version: str) -> "Definition":
        """Get definition by it's name and version.

        Args:
            rb_name (str): definition name
            rb_version (str): definition version

        Returns:
            Definition: Definition object

        """
        url: str = f"{cls.base_url_and_version()}/rb/definition/{rb_name}/{rb_version}"
        definition: dict = cls.send_message_json(
            "GET",
            "Get definition",
            url
        )
        return cls(
            definition["rb-name"],
            definition["rb-version"],
            definition.get("chart-name"),
            definition.get("description"),
            definition.get("labels")
        )

    @classmethod
    def create(cls, rb_name: str,
               rb_version: str,
               chart_name: str = "",
               description: str = "",
               labels=None) -> "Definition":
        """Create Definition.

        Args:
            rb_name (str): Definition name
            rb_version (str): Definition version
            chart_name (str): Chart name, optional field, will be detected if it is not provided
            description (str): Definition description
            labels (str): Labels

        Returns:
            Definition: Created object

        """
        if labels is None:
            labels = {}
        url: str = f"{cls.base_url_and_version()}/rb/definition"
        cls.send_message(
            "POST",
            "Create definition",
            url,
            data=jinja_env().get_template("multicloud_k8s_add_definition.json.j2").render(
                rb_name=rb_name,
                rb_version=rb_version,
                chart_name=chart_name,
                description=description,
                labels=labels
            )
        )
        return cls.get_definition_by_name_version(rb_name, rb_version)

    def update(self) -> "Definition":
        """Update Definition.

        Returns:
            Definition: Updated object

        """
        self.send_message(
            "PUT",
            "Update definition",
            self.url,
            data=jinja_env().get_template("multicloud_k8s_add_definition.json.j2").render(
                rb_name=self.rb_name,
                rb_version=self.rb_version,
                chart_name=self.chart_name,
                description=self.description,
                labels=self.labels
            )
        )
        return self.get_definition_by_name_version(self.rb_name, self.rb_version)

    def create_profile(self, profile_name: str,
                       namespace: str,
                       kubernetes_version: str,
                       release_name: str = None,
                       labels: dict = None,
                       extra_resource_types: list = None) -> "Profile":
        """Create Profile for Definition.

        Args:
            profile_name (str): Name of profile
            namespace (str): Namespace that service is created in
            kubernetes_version (str): Required Kubernetes version
            release_name (str): Release name
            labels (dict): Extra labels to assign for each
            extra_resource_types (list): GVK list for extra k8s resource types to check status

        Returns:
            Profile: Created object

        """
        url: str = f"{self.url}/profile"
        if release_name is None:
            release_name = profile_name
        if labels is None:
            labels = {}
        if extra_resource_types is None:
            extra_resource_types = []
        self.send_message(
            "POST",
            "Create profile for definition",
            url,
            data=jinja_env().get_template("multicloud_k8s_create_profile_"
                                          "for_definition.json.j2").render(
                                              rb_name=self.rb_name,
                                              rb_version=self.rb_version,
                                              profile_name=profile_name,
                                              release_name=release_name,
                                              namespace=namespace,
                                              kubernetes_version=kubernetes_version,
                                              labels=labels,
                                              extra_types=extra_resource_types
                                          )
        )
        return self.get_profile_by_name(profile_name)

    def get_all_profiles(self) -> Iterator["Profile"]:
        """Get all profiles.

        Yields:
            Profile: Profile object

        """
        url: str = f"{self.url}/profile"

        for profile in self.send_message_json("GET",
                                              "Get profiles",
                                              url):
            yield self.profile_class(
                profile["rb-name"],
                profile["rb-version"],
                profile["profile-name"],
                profile["namespace"],
                profile.get("kubernetes-version"),
                profile.get("labels"),
                profile.get("release-name"),
                GVK.to_list_of_gvk(profile.get("extra-resource-types"))
            )

    def get_profile_by_name(self, profile_name: str) -> "Profile":
        """Get profile by it's name.

        Args:
            profile_name (str): profile name

        Returns:
            Profile: Profile object

        """
        url: str = f"{self.url}/profile/{profile_name}"

        profile: dict = self.send_message_json(
            "GET",
            "Get profile",
            url
        )
        return self.profile_class(
            profile["rb-name"],
            profile["rb-version"],
            profile["profile-name"],
            profile["namespace"],
            profile.get("kubernetes-version"),
            profile.get("labels"),
            profile.get("release-name"),
            GVK.to_list_of_gvk(profile.get("extra-resource-types"))
        )

    def get_all_configuration_templates(self):
        """Get all configuration templates.

        Yields:
            ConfigurationTemplate: ConfigurationTemplate object

        """
        url: str = f"{self.url}/config-template"

        for template in self.send_message_json("GET",
                                               "Get configuration templates",
                                               url):
            yield self.config_template_class(
                self.rb_name,
                self.rb_version,
                template["template-name"],
                template.get("description"),
                template.get("chart-name"),
                template.get("has-content")
            )

    def create_configuration_template(self, template_name: str,
                                      description="") -> "ConfigurationTemplate":
        """Create configuration template.

        Args:
            template_name (str): Name of the template
            description (str): Description

        Returns:
            ConfigurationTemplate: Created object

        """
        url: str = f"{self.url}/config-template"

        self.send_message(
            "POST",
            "Create configuration template",
            url,
            data=jinja_env().get_template("multicloud_k8s_create_configuration_"
                                          "template.json.j2").render(
                                              template_name=template_name,
                                              description=description
                                          )
        )

        return self.get_configuration_template_by_name(template_name)

    def get_configuration_template_by_name(self, template_name: str) -> "ConfigurationTemplate":
        """Get configuration template.

        Args:
            template_name (str): Name of the template

        Returns:
            ConfigurationTemplate: object

        """
        url: str = f"{self.url}/config-template/{template_name}"

        template: dict = self.send_message_json(
            "GET",
            "Get Configuration template",
            url
        )
        return self.config_template_class(
            self.rb_name,
            self.rb_version,
            template["template-name"],
            template.get("description"),
            template.get("chart-name"),
            template.get("has-content")
        )
