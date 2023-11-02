"""VID module."""
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
from abc import ABC
from warnings import warn

from onapsdk.configuration import settings
from onapsdk.onap_service import OnapService
from onapsdk.utils.jinja import jinja_env


WARN_MSG = ("VID is deprecated and shouldn't be used! "
            "It's not a part of the ONAP release since Istanbul.")


class Vid(OnapService, ABC):
    """VID base class."""

    base_url = settings.VID_URL
    api_version = settings.VID_API_VERSION

    def __init__(self, name: str) -> None:
        """VID resource object initialization.

        Args:
            name (str): Resource name
        """
        warn(WARN_MSG)
        super().__init__()
        self.name: str = name

    @classmethod
    def get_create_url(cls) -> str:
        """Resource url.

        Used to create resources

        Returns:
            str: Url used for resource creation

        """
        raise NotImplementedError

    @classmethod
    def create(cls, name: str) -> "Vid":
        """Create VID resource.

        Returns:
            Vid: Created VID resource

        """
        warn(WARN_MSG)
        cls.send_message(
            "POST",
            f"Declare VID resource with {name} name",
            cls.get_create_url(),
            data=jinja_env().get_template("vid_declare_resource.json.j2").render(
                name=name
            )
        )
        return cls(name)


class OwningEntity(Vid):
    """VID owning entity class."""

    @classmethod
    def get_create_url(cls) -> str:
        """Owning entity creation url.

        Returns:
            str: Url used for ownint entity creation

        """
        warn(WARN_MSG)
        return f"{cls.base_url}{cls.api_version}/maintenance/category_parameter/owningEntity"


class Project(Vid):
    """VID project class."""

    @classmethod
    def get_create_url(cls) -> str:
        """Project creation url.

        Returns:
            str: Url used for project creation

        """
        warn(WARN_MSG)
        return f"{cls.base_url}{cls.api_version}/maintenance/category_parameter/project"


class LineOfBusiness(Vid):
    """VID line of business class."""

    @classmethod
    def get_create_url(cls) -> str:
        """Line of business creation url.

        Returns:
            str: Url used for line of business creation

        """
        warn(WARN_MSG)
        return f"{cls.base_url}{cls.api_version}/maintenance/category_parameter/lineOfBusiness"


class Platform(Vid):
    """VID platform class."""

    @classmethod
    def get_create_url(cls) -> str:
        """Platform creation url.

        Returns:
            str: Url used for platform creation

        """
        warn(WARN_MSG)
        return f"{cls.base_url}{cls.api_version}/maintenance/category_parameter/platform"
