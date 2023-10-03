"""A&AI link to project module."""
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
    from ..business.project import Project


class AaiResourceLinkToProjectMixin:  # pylint: disable=too-few-public-methods
    """Link aai resource to project mixin."""

    def link_to_project(self, project: "Project") -> None:
        """Create a relationship with project resource.

        Args:
            project (Project): Project object to create relationship with.

        """
        pro_relationship: Relationship = Relationship(
            related_to="project",
            related_link=project.url,
            relationship_data=[
                {
                    "relationship-key": "project.project-name",
                    "relationship-value": project.name,
                }
            ],
            relationship_label=RelationshipLabelEnum.PART_OF.value,
        )
        self.add_relationship(pro_relationship)

    def delete_relationship_with_project(self, project: "Project") -> None:
        """Delete relationship with project resource.

        Args:
            project (Project): Project object to delete relationship with.

        """
        proj_relationship: Relationship = Relationship(
            related_to="project",
            related_link=project.url,
            relationship_data=[
                {
                    "relationship-key": "project.project-name",
                    "relationship-value": project.name,
                }
            ],
            relationship_label=RelationshipLabelEnum.PART_OF.value,
        )
        self.delete_relationship(proj_relationship)
