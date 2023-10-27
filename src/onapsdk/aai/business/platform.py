"""A&AI platform module."""
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

from typing import Any, Dict, Iterator

from onapsdk.utils.jinja import jinja_env

from ..aai_element import AaiResource


class Platform(AaiResource):
    """Platform class."""

    def __init__(self, name: str, resource_version: str) -> None:
        """Platform object initialization.

        Args:
            name (str): Platform name
            resource_version (str): resource version
        """
        super().__init__()
        self.name: str = name
        self.resource_version: str = resource_version

    def __repr__(self) -> str:
        """Platform object representation.

        Returns:
            str: Platform object representation

        """
        return f"Platform(name={self.name})"

    @property
    def url(self) -> str:
        """Platform's url.

        Returns:
            str: Resource's url

        """
        return (f"{self.base_url}{self.api_version}/business/platforms/"
                f"platform/{self.name}")

    @classmethod
    def get_all_url(cls) -> str:  # pylint: disable=arguments-differ
        """Return url to get all platforms.

        Returns:
            str: Url to get all platforms

        """
        return f"{cls.base_url}{cls.api_version}/business/platforms"

    @classmethod
    def get_all(cls) -> Iterator["Platform"]:
        """Get all platform.

        Yields:
            Platform: Platform object

        """
        url: str = cls.get_all_url()
        for platform in cls.send_message_json("GET",
                                              "Get A&AI platforms",
                                              url).get("platform", []):
            yield cls(
                platform.get("platform-name"),
                platform.get("resource-version")
            )

    @classmethod
    def create(cls, name: str) -> "Platform":
        """Create platform A&AI resource.

        Args:
            name (str): platform name

        Returns:
            Platform: Created Platform object

        """
        cls.send_message(
            "PUT",
            "Declare A&AI platform",
            (f"{cls.base_url}{cls.api_version}/business/platforms/"
             f"platform/{name}"),
            data=jinja_env().get_template("aai_platform_create.json.j2").render(
                platform_name=name
            )
        )
        return cls.get_by_name(name)

    @classmethod
    def get_by_name(cls, name: str) -> "Platform":
        """Get platform resource by it's name.

        Raises:
            ResourceNotFound: Platform requested by a name does not exist.

        Returns:
            Platform: Platform requested by a name.

        """
        url = (f"{cls.base_url}{cls.api_version}/business/platforms/"
               f"platform/{name}")
        response: Dict[str, Any] = \
            cls.send_message_json("GET",
                                  f"Get {name} platform",
                                  url)
        return cls(response["platform-name"], response["resource-version"])

    def delete(self) -> None:
        """Delete platform."""
        self.send_message(
            "DELETE",
            "Delete platform",
            f"{self.url}?resource-version={self.resource_version}"
        )
