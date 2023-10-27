"""A&AI owning entity module."""
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

from uuid import uuid4
from typing import Iterator

from onapsdk.utils.jinja import jinja_env
from onapsdk.exceptions import ResourceNotFound

from ..aai_element import AaiResource

from ..mixins.link_to_tenant import AaiResourceLinkToTenantMixin


class OwningEntity(AaiResource, AaiResourceLinkToTenantMixin):
    """Owning entity class."""

    def __init__(self, name: str, owning_entity_id: str, resource_version: str) -> None:
        """Owning entity object initialization.

        Args:
            name (str): Owning entity name
            owning_entity_id (str): owning entity ID
            resource_version (str): resource version
        """
        super().__init__()
        self.name: str = name
        self.owning_entity_id: str = owning_entity_id
        self.resource_version: str = resource_version

    def __repr__(self) -> str:
        """Owning entity object representation.

        Returns:
            str: Owning entity object representation

        """
        return f"OwningEntity(name={self.name}, owning_entity_id={self.owning_entity_id})"

    @property
    def url(self) -> str:
        """Owning entity object url.

        Returns:
            str: Url

        """
        return (f"{self.base_url}{self.api_version}/business/owning-entities/owning-entity/"
                f"{self.owning_entity_id}")

    @classmethod
    def get_all_url(cls) -> str:  # pylint: disable=arguments-differ
        """Return url to get all owning entities.

        Returns:
            str: Url to get all owning entities

        """
        return f"{cls.base_url}{cls.api_version}/business/owning-entities"

    @classmethod
    def get_all(cls) -> Iterator["OwningEntity"]:
        """Get all owning entities.

        Yields:
            OwningEntity: OwningEntity object

        """
        url: str = cls.get_all_url()
        for owning_entity in cls.send_message_json("GET",
                                                   "Get A&AI owning entities",
                                                   url).get("owning-entity", []):
            yield cls(
                owning_entity.get("owning-entity-name"),
                owning_entity.get("owning-entity-id"),
                owning_entity.get("resource-version")
            )

    @classmethod
    def get_by_owning_entity_id(cls, owning_entity_id: str) -> "OwningEntity":
        """Get owning entity by it's ID.

        Args:
            owning_entity_id (str): owning entity object id

        Returns:
            OwningEntity: OwningEntity object

        """
        response: dict = cls.send_message_json(
            "GET",
            "Get A&AI owning entity",
            (f"{cls.base_url}{cls.api_version}/business/owning-entities/"
             f"owning-entity/{owning_entity_id}")
        )
        return cls(
            response.get("owning-entity-name"),
            response.get("owning-entity-id"),
            response.get("resource-version")
        )

    @classmethod
    def get_by_owning_entity_name(cls, owning_entity_name: str) -> "OwningEntity":
        """Get owning entity resource by it's name.

        Raises:
            ResourceNotFound: Owning entity requested by a name does not exist.

        Returns:
            OwningEntity: Owning entity requested by a name.

        """
        for owning_entity in cls.get_all():
            if owning_entity.name == owning_entity_name:
                return owning_entity

        msg = f'Owning entity "{owning_entity_name}" does not exist.'
        raise ResourceNotFound(msg)

    @classmethod
    def create(cls, name: str, owning_entity_id: str = None) -> "OwningEntity":
        """Create owning entity A&AI resource.

        Args:
            name (str): owning entity name
            owning_entity_id (str): owning entity ID. Defaults to None.

        Returns:
            OwningEntity: Created OwningEntity object

        """
        if not owning_entity_id:
            owning_entity_id = str(uuid4())
        cls.send_message(
            "PUT",
            "Declare A&AI owning entity",
            (f"{cls.base_url}{cls.api_version}/business/owning-entities/"
             f"owning-entity/{owning_entity_id}"),
            data=jinja_env().get_template("aai_owning_entity_create_update.json.j2").render(
                owning_entity_name=name,
                owning_entity_id=owning_entity_id
            )
        )
        return cls.get_by_owning_entity_id(owning_entity_id)

    @classmethod
    def update(cls, name: str, owning_entity_id: str) -> "OwningEntity":
        """Update owning entity A&AI resource.

        Args:
            name (str): owning entity name
            owning_entity_id (str): owning entity ID.

        Returns:
            OwningEntity: Updated OwningEntity object

        """
        cls.send_message(
            "PATCH",
            "update A&AI owning entity",
            (f"{cls.base_url}{cls.api_version}/business/owning-entities/"
             f"owning-entity/{owning_entity_id}"),
            data=jinja_env().get_template("aai_owning_entity_create_update.json.j2").render(
                owning_entity_name=name,
                owning_entity_id=owning_entity_id
            )
        )
        return cls.get_by_owning_entity_id(owning_entity_id)

    def delete(self) -> None:
        """Delete owning entity.

        Sends request to A&AI to delete owning entity object.

        """
        self.send_message(
            "DELETE",
            "Delete owning entity",
            f"{self.url}?resource-version={self.resource_version}"
        )
