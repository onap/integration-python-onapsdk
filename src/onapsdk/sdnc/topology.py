"""SDNC topology module. NETCONF-API."""
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
from typing import Dict, Iterable

from onapsdk.utils.headers_creator import headers_sdnc_creator
from onapsdk.utils.jinja import jinja_env

from .sdnc_element import SdncElement

class Tplg(SdncElement):
    """SDNC topology base class."""

    headers: Dict[str, str] = headers_sdnc_creator(SdncElement.headers)

class Topology(Tplg):
    """SDNC topology."""

    def __init__(self,
                 topology_id: str):
        """Topology information initialization.

        Args:
            topology_id (str):  Topology instance id
        """
        super().__init__()
        self.topology_id: str = topology_id

    def __repr__(self) -> str:
        """Service information human readable string.

        Returns:
            str: Node information description

        """
        return f"Topology(topology_id={self.topology_id})"

    @classmethod
    def get_network_topology(cls) -> Iterable["Service"]:
        """Get all network topology using NETCONF-API.

        Yields:
            : Topology object
        """
        for topology in \
            cls.send_message_json(\
                "GET",\
                "Get SDNC services",\
                f"{cls.base_url}/rests/data/network-topology:network-topology"
                                 ).get("network-topology:network-topology", {}
                                       ).get('topology', []):
            yield Topology(topology_id=topology["topology-id"])

class Node(Topology):
    """SDNC topology."""

    def __init__(self,
                 topology_id: str,
                 node_id: str):
        """Node information initialization.

        Args:
            Topology_id (str):  Topology instance id
            Node_id (str):  Node instance id
        """
        super().__init__(topology_id)
        self.topology_id: str = topology_id
        self.node_id: str = node_id
    def __repr__(self) -> str:
        """Node information human readable string.

        Returns:
            str: Node information description

        """
        return f"Node(topology_id={self.topology_id},node_id={self.node_id})"

    def create(self) -> None:
        """Create node using NETCONF-API."""
        self.send_message(
            "POST",
            "Create a node using NETCONF-API",
            (f"{self.base_url}/rests/data/"
             f"network-topology:network-topology/topology={self.topology_id}"),
            data=jinja_env().get_template(
                "create_node_netconf_api.json.j2").
            render(
                node_id=self.node_id
            )
        )

    def get(self) -> None:
        """Get information about node using NETCONF-API."""
        for node in \
                self.send_message_json(
                        "GET",
                        "Get information about service using NETCONF-API",
                        (f"{self.base_url}/rests/data/"
                         f"network-topology:network-topology/topology={self.topology_id}"
                         f"/node={self.node_id}")
                ).get('network-topology:node', []):
            yield Node(topology_id=self.topology_id, node_id=node["node-id"])

    def delete(self) -> None:
        """Delete node using NETCONF-API."""
        self.send_message(
            "DELETE",
            "DELETE a node using NETCONF-API",
            (f"{self.base_url}/rests/data/"
             f"network-topology:network-topology/topology={self.topology_id}"
             f"/node={self.node_id}")
        )
