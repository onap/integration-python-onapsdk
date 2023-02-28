"""Neigbour module."""
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

from typing import Iterator, Optional

from onapsdk.utils.jinja import jinja_env

from ..aai_element import AaiResource


class Neighbour(AaiResource):  # pylint: disable=too-many-instance-attributes
    """Neigbour class."""

    def __init__(self,
                 neighbour_id: str,
                 *,
                 neighbour_cell_name: str = "",
                 neighbour_cell_id: str = "",
                 selflink: str = "",
                 data_owner: str = "",
                 data_source: str = "",
                 data_source_version: str = "",
                 resource_version: str = "",
                 ) -> None:
        """Neigbour init.

        Args:
            neighbour_id (str): UUID, key for neighbour object.
            neighbour_cell_name (str, optional): Name of neighbour. Defaults to "".
            neighbour_cell_id (str, optional): Type of neighbour. Defaults to "".
            selflink (str, optional): Role of neighbour. Defaults to "".
            data_owner (str, optional): Identifies the entity that is responsible managing
                this inventory object. Defaults to "".
            data_source (str, optional): Identifies the upstream source of the data.
                Defaults to "".
            data_source_version (str, optional): Identifies the version of
                the upstream source. Defaults to "".
            resource_version (str, optional): Resource version. Defaults to "".

        """
        super().__init__()
        self.neighbour_id: str = neighbour_id
        self.neighbour_cell_name: str = neighbour_cell_name
        self.neighbour_cell_id: str = neighbour_cell_id
        self.selflink: str = selflink
        self.data_owner: str = data_owner
        self.data_source: str = data_source
        self.data_source_version: str = data_source_version
        self.resource_version: str = resource_version

    def __repr__(self) -> str:
        """Neigbour object representation.

        Returns:
            str: Human readable string contains most important information about Neigbour.

        """
        return (
            f"Neighbour(neighbour_id={self.neighbour_id})"
        )

    @property
    def url(self) -> str:
        """Neighbours url.

        Returns:
            str: Neighbours url

        """
        return (f"{self.base_url}{self.api_version}/cloud-infrastructure/"
                f"neighbours/neighbour/{self.neighbour_id}")

    @classmethod
    def get_all_url(cls, *args, **kwargs) -> str:  # pylint: disable=arguments-differ
        """Return url to get all neighbours.

        Returns:
            str: Url to get all neighbours

        Raises:
            ResourceNotFound: No neighbours found

        """
        return f"{cls.base_url}{cls.api_version}/cloud-infrastructure/neighbours"

    @classmethod
    def get_all(cls) -> Iterator["Neighbour"]:
        """Get all neighbours.

        Yields:
            Neighbour: Neigbour

        """
        for neighbour_data in cls.send_message_json("GET",
                                                     "Get all neighbours",
                                                     cls.get_all_url()).get("neighbour", []):
            yield cls(neighbour_id=neighbour_data["neighbour-id"],
                      neighbour_cell_name=neighbour_data.get("neighbour-name", ""),
                      neighbour_cell_id=neighbour_data.get("neighbour-type", ""),
                      selflink=neighbour_data.get("neighbour-role", ""),
                      data_owner=neighbour_data.get("data-owner", ""),
                      data_source=neighbour_data.get("data-source", ""),
                      data_source_version=neighbour_data.get("data-source-version", ""),
                      resource_version=neighbour_data.get("resource-version", ""))

    @classmethod
    def get_by_neighbour_id(cls, neighbour_id: str) -> "Neighbour":
        """Get Neigbour by it's id.

        Args:
            neighbour_id (str): Neigbour id

        Returns:
            Neighbour: Neigbour

        """
        resp = cls.send_message_json("GET",
                                     f"Get Neigbour with {neighbour_id} id",
                                     f"{cls.get_all_url()}/neighbour/{neighbour_id}")
        return Neighbour(resp["neighbour-id"],
                         neighbour_cell_name=resp.get("neighbour-name", ""),
                         neighbour_cell_id=resp.get("neighbour-type", ""),
                         selflink=resp.get("neighbour-role", ""),
                         data_owner=resp.get("data-owner", ""),
                         data_source=resp.get("data-source", ""),
                         data_source_version=resp.get("data-source-version", ""),
                         resource_version=resp["resource-version"])

    @classmethod
    def create(cls,  # pylint: disable=too-many-arguments
               neighbour_id: str,
               neighbour_cell_name: Optional[str] = None,
               neighbour_cell_id: Optional[str] = None,
               selflink: Optional[str] = None,
               data_owner: Optional[str] = None,
               data_source: Optional[str] = None,
               data_source_version: Optional[str] = None) -> "Neighbour":
        """Create Neigbour.

        Args:
            neighbour_id (str): UUID, key for neighbour object.
            neighbour_cell_name (Optional[str], optional): Name of neighbour. Defaults to None.
            neighbour_cell_id (Optional[str], optional): Type of neighbour. Defaults to None.
            selflink (Optional[str], optional): Role of neighbour. Defaults to None.
            data_owner (Optional[str], optional): Identifies the entity that is
                responsible managing this inventory object.. Defaults to None.
            data_source (Optional[str], optional): Identifies the upstream source of the data.
                Defaults to None.
            data_source_version (Optional[str], optional): Identifies the version of
                the upstream source. Defaults to None.

        Returns:
            Neighbour: Neigbour object

        """
        cls.send_message(
            "PUT",
            "Create Neigbour",
            f"{cls.get_all_url()}/neighbour/{neighbour_id}",
            data=jinja_env()
            .get_template("neighbour_create.json.j2")
            .render(neighbour_id=neighbour_id,
                    neighbour_cell_name=neighbour_cell_name,
                    neighbour_cell_id=neighbour_cell_id,
                    selflink=selflink,
                    data_owner=data_owner,
                    data_source=data_source,
                    data_source_version=data_source_version),
        )
        return cls.get_by_neighbour_id(neighbour_id)

    def delete(self) -> None:
        """Delete neighbour."""
        self.send_message(
            "DELETE",
            f"Delete {self.neighbour_id} neighbour",
            f"{self.url}?resource-version={self.resource_version}"
        )