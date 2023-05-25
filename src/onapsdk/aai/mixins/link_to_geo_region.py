"""A&AI link to geo region mixin module."""
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
    from ..cloud_infrastructure.geo_region import GeoRegion

class AaiResourceLinkToGeoRegionMixin:  # pylint: disable=too-few-public-methods
    """Link aai resource to geo region mixin."""

    def link_to_geo_region(self, geo_region: "GeoRegion") -> None:
        """Create a relationship with geo region.

        As few resources create same relationship with geo region

        Args:
            geo_region (GeoRegion): Geo region object
        """
        relationship: Relationship = Relationship(
            related_to="geo-region",
            related_link=geo_region.url,
            relationship_data=[
                {
                    "relationship-key": "geo-region.geo-region-id",
                    "relationship-value": geo_region.geo_region_id,
                }
            ],
            relationship_label=RelationshipLabelEnum.MEMBER_OF.value,
        )
        self.add_relationship(relationship)
