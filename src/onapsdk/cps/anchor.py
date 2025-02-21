"""ONAP SDK CPS anchor module."""
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

from typing import Any, Dict, TYPE_CHECKING
from urllib.parse import urljoin

from .cps_element import CpsElement

if TYPE_CHECKING:
    from .schemaset import SchemaSet  # pylint: disable=cyclic-import


class Anchor(CpsElement):
    """CPS anchor class."""

    def __init__(self, name: str, schema_set: "SchemaSet") -> None:
        """Initialise CPS anchor object.

        Args:
            name (str): Anchor name
            schema_set (SchemaSet): Schema set

        """
        super().__init__()
        self.name: str = name
        self.schema_set: "SchemaSet" = schema_set

    def __repr__(self) -> str:
        """Human readable representation of the object.

        Returns:
            str: Human readable string

        """
        return (
            f"Anchor(name={self.name}, "
            f"schema set={self.schema_set.name}, "
            f"dataspace={self.schema_set.dataspace.name})"
        )

    @property
    def url(self) -> str:
        """Anchor url.

        Returns:
            str: Anchor url

        """
        return urljoin(self._url,
                       f"dataspaces/{self.schema_set.dataspace.name}/anchors/{self.name}/")

    def delete(self) -> None:
        """Delete anchor."""
        # For some reason CPS API does not strip ending '/' character so it has to be removed here.
        self.send_message(
            "DELETE", f"Delete {self.name} anchor", self.url.rstrip("/"), auth=self.auth
        )

    def create_node(self, node_data: str) -> None:
        """Create anchor node.

        Fill CPS anchor with a data.

        Args:
            node_data (str): Node data. Should be JSON formatted.

        """
        self.send_message(
            "POST",
            f"Create {self.name} anchor node",
            urljoin(self.url, "nodes"),
            data=node_data,
            auth=self.auth,
        )

    def get_node(self, xpath: str, descendants: int = 0) -> Dict[Any, Any]:
        """
        Get anchor node data.

        Using XPATH get anchor's node data.

        Args:
            xpath (str): Anchor node xpath.
            descendants (int, optional): Determines the number of descendant
                levels that should be returned.
                Can be -1 (all), 0 (none), or any positive number.
                Defaults to 0.
        Returns:
            Dict[Any, Any]: Anchor node data.
        """
        return self.send_message_json(
            "GET",
            f"Get {self.name} anchor node with {xpath} xpath",
            urljoin(self.url, "node"),
            params={"xpath": xpath,
                    "descendants": descendants},
            auth=self.auth
        )


    def update_node(self, xpath: str, node_data: str) -> None:
        """Update anchor node data.

        Using XPATH, update
        anchor's node data.

        Args:
            xpath (str): Anchor node xpath.
            node_data (str): Node data.

        """
        self.send_message(
            "PATCH",
            f"Update {self.name} anchor node with {xpath} xpath",
            urljoin(self.url, "nodes"),
            params={"xpath": xpath},
            data=node_data,
            auth=self.auth,
        )

    def replace_node(self, xpath: str, node_data: str) -> None:
        """Replace anchor node data.

        Using XPATH replace anchor's node data.

        Args:
            xpath (str): Anchor node xpath.
            node_data (str): Node data.

        """
        self.send_message(
            "PUT",
            f"Replace {self.name} anchor node with {xpath} xpath",
            urljoin(self.url, "nodes"),
            params={"xpath": xpath},
            data=node_data,
            auth=self.auth,
        )

    def add_list_node(self, xpath: str, node_data: str) -> None:
        """Add an element to the list node of an anchor.

        Args:
            xpath (str): Xpath to the list node.
            node_data (str): Data to be added.

        """
        self.send_message(
            "POST",
            f"Add element to {self.name} anchor node with {xpath} xpath",
            urljoin(self.url, "list-nodes"),
            params={"xpath": xpath},
            data=node_data,
            auth=self.auth,
        )

    def query_node(
            self, query: str, include_descendants: bool = False
    ) -> Dict[Any, Any]:
        """Query CPS anchor data.

        Args:
            query (str): Query
            include_descendants (bool, optional): Determines if descendants should be included in
                response. Defaults to False.

        Returns:
            Dict[Any, Any]: Query return values.

        """
        return self.send_message_json(
            "GET",
            f"Get {self.name} anchor node with {query} query",
            urljoin(self.url, "nodes/query"),
            params={"cps-path": query,
                    "include-descendants": include_descendants},
            auth=self.auth,
        )

    def delete_nodes(self, xpath: str) -> None:
        """Delete nodes.

        Use XPATH to delete Anchor nodes.

        Args:
            xpath (str): Nodes to delete

        """
        self.send_message(
            "DELETE",
            f"Delete {self.name} anchor nodes with {xpath} xpath",
            urljoin(self.url, "nodes"),
            params={"xpath": xpath},
            auth=self.auth,
        )

    def delta(self, data: dict, xpath: str = "/") -> None:
        """Get node delta.

        Use delta feature to get the difference between the anchor's node
            data and the data sent in the request

        Args:
            data (dict): Data to be sent to CPS.
            xpath (str, optional): Anchor xpath. Defaults to "/".

        """
        self.send_message_json("POST",
                          f"Get {self.name} anchor node delta for {xpath} xpath",
                          f"{urljoin(self.url, 'delta')}",
                          params={"xpath": xpath},
                          auth=self.auth,
                          headers={},
                          files={"json": (None, data)})
