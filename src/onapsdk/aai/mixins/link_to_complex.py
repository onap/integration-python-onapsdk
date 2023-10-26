"""A&AI link to complex module."""
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

from typing import Optional, TYPE_CHECKING

from onapsdk.exceptions import ResourceNotFound

from ..aai_element import Relationship, RelationshipLabelEnum

if TYPE_CHECKING:
    from ..cloud_infrastructure.complex import Complex


class AaiResourceLinkToComplexMixin:  # pylint: disable=too-few-public-methods
    """Link aai resource to complex mixin."""

    RELATED_TO: str = "complex"

    def link_to_complex(self, cmplx: "Complex",
                        relationship_label: RelationshipLabelEnum = \
                                RelationshipLabelEnum.LOCATED_IN) -> None:
        """Create a relationship with complex resource.

        Args:
            cmplx (Complex): Complex object ot create relationship with.

        """
        relationship: Relationship = Relationship(
            related_to=self.RELATED_TO,
            related_link=cmplx.url,
            relationship_data=[
                {
                    "relationship-key": "complex.physical-location-id",
                    "relationship-value": cmplx.physical_location_id,
                }
            ],
            relationship_label=relationship_label.value,
        )
        self.add_relationship(relationship)

    def unlink_complex(self, cmplx: "Complex") -> None:
        """Delete relationship with complex resource.

        If relationship doesn't exist do nothing.

        Args:
            cmplx (Complex): Complex object to delete relationship with.

        """
        try:
            for relationship in self.relationships:
                if relationship.related_to == self.RELATED_TO:
                    physical_location_id: Optional[str] = relationship.get_relationship_data(
                        "complex.physical-location-id"
                    )
                    if physical_location_id is not None \
                            and cmplx.physical_location_id == physical_location_id:
                        self._logger.debug(f"Delete relationship with {cmplx.physical_location_id} "
                                           "complex")
                        self.delete_relationship(relationship)
                        break
        except ResourceNotFound:
            self._logger.debug("Resource has no relationships")
