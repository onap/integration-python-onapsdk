"""AAI Element module."""
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
import enum
from dataclasses import dataclass, field
from typing import Dict, Iterator, List, Optional

from onapsdk.configuration import settings
from onapsdk.onap_service import OnapService
from onapsdk.utils.headers_creator import headers_aai_creator
from onapsdk.utils.jinja import jinja_env
from onapsdk.utils.gui import GuiItem, GuiList

from onapsdk.exceptions import RelationshipNotFound, ResourceNotFound


@dataclass
class Relationship:
    """Relationship class.

    A&AI elements could have relationship with other A&AI elements.
    Relationships are represented by this class objects.
    """

    related_to: str
    related_link: str
    relationship_data: List[Dict[str, str]]
    relationship_label: str = ""
    related_to_property: List[Dict[str, str]] = field(default_factory=list)

    def get_relationship_data(self, relationship_key: str) -> Optional[str]:
        """Get relationship data for given relationship key.

        From list of relationship data get the value for
            given key

        Args:
            relationship_key (str): Key to get relationship data value

        Returns:
            Optional[str]: Relationship value or None if relationship data
                with provided ket doesn't exist

        """
        for data in self.relationship_data:
            if data["relationship-key"] == relationship_key:
                return data["relationship-value"]
        return None


@enum.unique
class RelationshipLabelEnum(enum.Enum):
    """Class to hold relationship labels."""

    APPLIES_TO = "org.onap.relationships.inventory.AppliesTo"
    BELONGS_TO = "org.onap.relationships.inventory.BelongsTo"
    BINDS_TO = "org.onap.relationships.inventory.BindsTo"
    CAN_BE_INSTANTIATED_IN = "org.onap.relationships.inventory.CanBeInstantiatedIn"
    COMPOSED_OF = "org.onap.relationships.inventory.ComposedOf"
    CONTROLLED_BY = "org.onap.relationships.inventory.ControlledBy"
    DEPENDS_ON = "org.onap.relationships.inventory.DependsOn"
    DESTINATION = "org.onap.relationships.inventory.Destination"
    FORWARDS_TO = "org.onap.relationships.inventory.ForwardsTo"
    IS_A = "org.onap.relationships.inventory.IsA"
    IMPLEMENTS = "org.onap.relationships.inventory.Implements"
    LINKS_TO = "org.onap.relationships.inventory.LinksTo"
    LOCATED_IN = "org.onap.relationships.inventory.LocatedIn"
    MEMBER_OF = "org.onap.relationships.inventory.MemberOf"
    NETWORK_APPLIES_TO = "org.onap.relationships.inventory.network.AppliesTo"
    NETWORK_BELONGS_TO = "org.onap.relationships.inventory.network.BelongsTo"
    NETWORK_MEMBER_OF = "org.onap.relationships.inventory.network.MemberOf"
    NETWORK_USES = "org.onap.relationships.inventory.network.Uses"
    PART_OF = "org.onap.relationships.inventory.PartOf"
    PRIMARY = "org.onap.relationships.inventory.Primary"
    SECONDARY = "org.onap.relationships.inventory.Secondary"
    SOURCE = "org.onap.relationships.inventory.Source"
    SUPPORTS = "org.onap.relationships.inventory.Supports"
    TARGET = "org.onap.relationships.inventory.Target"
    TARGETS = "org.onap.relationships.inventory.Targets"
    USES = "org.onap.relationships.inventory.Uses"


class AaiElement(OnapService):
    """Mother Class of all A&AI elements."""

    name: str = "AAI"
    server: str = "AAI"
    base_url = settings.AAI_URL
    api_version = "/aai/" + settings.AAI_API_VERSION
    headers = headers_aai_creator(OnapService.headers)
    patch_headers = headers_aai_creator({
        "Content-Type": "application/merge-patch+json",
        "Accept": "application/json",
    })

    @classmethod
    def get_guis(cls) -> GuiList:
        """Retrieve the status of the AAI GUIs.

        Only one GUI is referenced for AAI
        the AAI sparky GUI

        Return the list of GUIs
        """
        gui_url = settings.AAI_GUI_SERVICE
        aai_gui_response = cls.send_message(
            "GET", "Get AAI GUI Status", gui_url)
        guilist = GuiList([])
        guilist.add(GuiItem(
            gui_url,
            aai_gui_response.status_code))
        return guilist


class AaiResource(AaiElement):
    """A&AI resource class."""

    @classmethod
    def filter_none_key_values(cls, dict_to_filter: Dict[str, Optional[str]]) -> Dict[str, str]:
        """Filter out None key values from dictionary.

        Iterate through given dictionary and filter None values.

        Args:
            dict_to_filter (Dict): Dictionary to filter out None

        Returns:dataclasse init a field
            Dict[str, str]: Filtered dictionary

        """
        return dict(
            filter(lambda key_value_tuple: key_value_tuple[1] is not None, dict_to_filter.items(),)
        )

    @property
    def url(self) -> str:
        """Resource's url.

        Returns:
            str: Resource's url

        """
        raise NotImplementedError

    @property
    def relationships(self) -> Iterator[Relationship]:
        """Resource relationships iterator.

        Yields:
            Relationship: resource relationship

        Raises:
            RelationshipNotFound: if request for relationships returned 404

        """
        try:
            generator = self.send_message_json("GET",
                                               "Get object relationships",
                                               f"{self.url}/relationship-list")\
                                                   .get("relationship", [])
            for relationship in generator:
                yield Relationship(
                    related_to=relationship.get("related-to"),
                    relationship_label=relationship.get("relationship-label"),
                    related_link=relationship.get("related-link"),
                    relationship_data=relationship.get("relationship-data"),
                )
        except ResourceNotFound as exc:
            self._logger.error("Getting object relationships failed: %s", exc)

            msg = (f'{self.name} relationships not found.'
                   f'Server: {self.server}. Url: {self.url}')
            raise RelationshipNotFound(msg) from exc

    @classmethod
    def get_all_url(cls, *args, **kwargs) -> str:
        """Return an url for all objects of given class.

        Returns:
            str: URL to get all objects of given class

        """
        raise NotImplementedError

    @classmethod
    def count(cls, *args, **kwargs) -> int:
        """Get the count number of all objects of given class.

        Get the response, iterate through response (each class has different response)
            -- the first key value is the count.

        Returns:
            int: Count of the objects

        """
        return next(iter(cls.send_message_json(
            "GET",
            f"Get count of {cls.__name__} class instances",
            f"{cls.get_all_url(*args, **kwargs)}?format=count"
        )["results"][0].values()))

    def add_relationship(self, relationship: Relationship) -> None:
        """Add relationship to aai resource.

        Add relationship to resource using A&AI API

        Args:
            relationship (Relationship): Relationship to add

        """
        self._logger.info("Adding relationship to aai resource")
        self.send_message(
            "PUT",
            f"add relationship to {self.__class__.__name__}",
            f"{self.url}/relationship-list/relationship",
            data=jinja_env()
            .get_template("aai_add_relationship.json.j2")
            .render(relationship=relationship),
        )

    def delete_relationship(self, relationship: Relationship) -> None:
        """Delete relationship from aai resource.

        Delete relationship from resource using A&AI API

        Args:
            relationship (Relationship): Relationship to delete

        """
        self._logger.info("Deleting relationship from aai resource")
        self.send_message(
            "DELETE",
            f"delete relationship from {self.__class__.__name__}",
            f"{self.url}/relationship-list/relationship",
            data=jinja_env()
            .get_template("aai_delete_relationship.json.j2")
            .render(relationship=relationship),
        )
