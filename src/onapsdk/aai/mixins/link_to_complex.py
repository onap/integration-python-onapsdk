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

from typing import TYPE_CHECKING

from ..aai_element import Relationship, RelationshipLabelEnum

if TYPE_CHECKING:
    from ..cloud_infrastructure.complex import Complex


class AaiResourceLinkToComplexMixin:  # pylint: disable=too-few-public-methods
    """Link aai resource to complex mixin."""

    def link_to_complex(self, cmplx: "Complex",
                        relationship_label: RelationshipLabelEnum =\
                            RelationshipLabelEnum.LOCATED_IN) -> None:
        """Create a relationship with complex resource.

        Args:
            cmplx (Complex): Complex object ot create relationship with.

        """
        relationship: Relationship = Relationship(
            related_to="complex",
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
