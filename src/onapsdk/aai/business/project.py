"""A&AI project module."""
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


class Project(AaiResource):
    """Project class."""

    def __init__(self, name: str, resource_version: str) -> None:
        """Project object initialization.

        Args:
            name (str): Project name
            resource_version (str): resource version
        """
        super().__init__()
        self.name: str = name
        self.resource_version: str = resource_version

    @classmethod
    def get_all(cls) -> Iterator["Project"]:
        """Get all project.

        Yields:
            Project: Project object

        """
        url: str = cls.get_all_url()
        for project in cls.send_message_json("GET",
                                             "Get A&AI projects",
                                             url).get("project", []):
            yield cls(
                project.get("project-name"),
                project.get("resource-version")
            )

    @classmethod
    def get_all_url(cls) -> str:  # pylint: disable=arguments-differ
        """Return url to get all projects.

        Returns:
            str: Url to get all projects

        """
        return f"{cls.base_url}{cls.api_version}/business/projects"

    def __repr__(self) -> str:
        """Project object representation.

        Returns:
            str: Project object representation

        """
        return f"Project(name={self.name})"

    @property
    def url(self) -> str:
        """Project's url.

        Returns:
            str: Resource's url

        """
        return (f"{self.base_url}{self.api_version}/business/projects/"
                f"project/{self.name}")

    @classmethod
    def create(cls, name: str) -> "Project":
        """Create project A&AI resource.

        Args:
            name (str): project name

        Returns:
            Project: Created Project object

        """
        cls.send_message(
            "PUT",
            "Declare A&AI project",
            (f"{cls.base_url}{cls.api_version}/business/projects/"
             f"project/{name}"),
            data=jinja_env().get_template("aai_project_create.json.j2").render(
                project_name=name
            )
        )
        return cls.get_by_name(name)

    @classmethod
    def get_by_name(cls, name: str) -> "Project":
        """Get project resource by it's name.

        Raises:
            ResourceNotFound: Project requested by a name does not exist.

        Returns:
            Project: Project requested by a name.

        """
        url = (f"{cls.base_url}{cls.api_version}/business/projects/"
               f"project/{name}")
        response: Dict[str, Any] = \
            cls.send_message_json("GET",
                                  f"Get {name} project",
                                  url)
        return cls(response["project-name"], response["resource-version"])

    def delete(self) -> None:
        """Delete project."""
        self.send_message(
            "DELETE",
            "Delete project",
            f"{self.url}?resource-version={self.resource_version}"
        )
