"""SDNC topology module. NETCONF-API."""
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
from typing import List, Dict, Iterable, Optional

from onapsdk.utils.headers_creator import headers_sdnc_creator
from onapsdk.utils.jinja import jinja_env

from .sdnc_element import SdncElement


NETCONF_NODE_TOPOLOGY_HOST: str = "netconf-node-topology:host"
NETCONF_NODE_TOPOLOGY_PORT: str = "netconf-node-topology:port"
NETCONF_NODE_TOPOLOGY_USERNAME: str = "netconf-node-topology:username"
NETCONF_NODE_TOPOLOGY_PASSWORD: str = "netconf-node-topology:password"


class Node(SdncElement):
    """SDNC Node."""

    headers: Dict[str, str] = headers_sdnc_creator(SdncElement.headers)

    def __init__(self,  # pylint: disable=too-many-arguments
                 node_id: str,
                 host: str,
                 port: int,
                 username: str,
                 password: str,
                 topology_id: str = "topology-netconf",
                 **kwargs) -> None:
        """Node information initialization.

        Args:
            node_id (str):  Node id,
            host (str):  Node IPv4 address,
            port (int):  Node Netconf port number,
            username (str):  Node username,
            password (str):  Node password,
            topology_id: (str) : Topology, where node is contained
            data (Dict):  other possible Node data,

        """
        super().__init__()
        self.node_id: str = node_id
        self.host: str = host
        self.port: int = port
        self.username: str = username
        self.password: str = password
        self.topology_id: str = topology_id
        self.data: Dict = kwargs

    def __repr__(self) -> str:
        """Node information human-readable string.

        Returns:
            str: Node information description
        """
        return f"Node(node_id={self.node_id}," \
               f"host={self.host}," \
               f"port={self.port}," \
               f"username={self.username}," \
               f"password={self.password}," \
               f"data={self.data})"

    def create(self) -> None:
        """Create the node element of the topology at SDNC via NETCONF-API.

        Returns:
            None
        """
        node_json_template = {
            "node": {
                "node-id": "",
                NETCONF_NODE_TOPOLOGY_HOST: "",
                NETCONF_NODE_TOPOLOGY_PORT: 0,
                NETCONF_NODE_TOPOLOGY_USERNAME: "",
                NETCONF_NODE_TOPOLOGY_PASSWORD: ""
            }
        }
        self.send_message(
            "POST",
            "Add a node element into the topology at SDNC using NETCONF-API",
            (f"{self.base_url}/rests/data/"
             f"network-topology:network-topology/topology={self.topology_id}"),
            data=jinja_env().get_template(
                "create_node_netconf_api.json.j2").
            render(
                node_json_template,
                node_id=self.node_id,
                host_=self.host,
                port_=self.port,
                username_=self.username,
                password_=self.password
            )
        )

    def update(self) -> None:
        """Update the node element of the topology at SDNC via NETCONF-API.

        Returns:
            None

        """
        node_json_template = {
            "node": {
                "node-id": "",
                NETCONF_NODE_TOPOLOGY_HOST: "",
                NETCONF_NODE_TOPOLOGY_PORT: 0,
                NETCONF_NODE_TOPOLOGY_USERNAME: "",
                NETCONF_NODE_TOPOLOGY_PASSWORD: ""
            }
        }
        self.send_message(
            "PUT",
            "Add a Node element into the topology using NETCONF-API",
            (f"{self.base_url}/rests/data/"
             f"network-topology:network-topology/topology={self.topology_id}"
             f"/node={self.node_id}"),
            data=jinja_env().get_template(
                "create_node_netconf_api.json.j2").
            render(
                node_json_template,
                node_id=self.node_id,
                host_=self.host,
                port_=self.port,
                username_=self.username,
                password_=self.password)
        )

    def delete(self) -> None:
        """Delete the node element of the topology from SDNC via NETCONF-API.

        Returns:
            None

        """
        self.send_message(
            "DELETE",
            "Delete a Node element from the topology using NETCONF-API",
            (f"{self.base_url}/rests/data/"
             f"network-topology:network-topology/topology={self.topology_id}"
             f"/node={self.node_id}")
        )


class Topology(SdncElement):
    """SDNC topology."""

    headers: Dict[str, str] = headers_sdnc_creator(SdncElement.headers)

    def __init__(self,
                 topology_id: str = "topology-netconf",
                 nodes: List[Node] = None):
        """Topology information initialization.

        Args:
            topology_id (str):  Topology instance id
            nodes (list): List of nodes inside the topology
        """
        super().__init__()
        self.topology_id: str = topology_id
        self.nodes: list = nodes

    def __repr__(self) -> str:
        """Topology information human-readable string.

        Returns:
            str: Topology information description

        """
        return f"Topology(topology_id={self.topology_id}," \
               f"nodes={self.nodes})"

    @classmethod
    def get_all(cls) -> Iterable["Topology"]:
        """Get all topologies from SDNC using NETCONF-API.

        Yields:
            : Topology object
        """
        topologies = cls.send_message_json("GET",
                                           "Get all topologies from SDNC using NETCONF-API",
                                           f"{cls.base_url}"
                                           f"/rests/data/network-topology:network-topology"
                                           ).get("network-topology:network-topology", {}
                                                 ).get("topology", [])
        for topology in topologies:
            try:
                yield Topology(topology_id=topology["topology-id"], nodes=topology["node"])
            except KeyError:
                print(f"Topology with topology-id={topology['topology-id']}"
                      f" doesn't contain any node")
                yield Topology(topology_id=topology["topology-id"])

    @classmethod
    def get(cls, topology_id) -> "Topology":
        """Get the topology with a specific topology_id from SDNC via NETCONF-API.

        Returns:
            Topology

        """
        topology_object = cls.send_message_json("GET",
                                                "Get all topologies from SDNC using NETCONF-API",
                                                f"{cls.base_url}"
                                                f"/rests/data/network-topology:network-topology/"
                                                f"topology={topology_id}"
                                                )
        try:
            topology = topology_object["network-topology:topology"][0]
            return Topology(topology_id=topology["topology-id"],
                            nodes=topology["node"]
                            )
        except KeyError:
            return Topology(topology_id=topology_id)

    def get_node(self, node_id) -> Optional["Node"]:
        """Get the node with a specific node_id form the specific topology at SDNC via NETCONF-API.

        Returns:
            Node

        """
        node_object = self.send_message_json("GET",
                                             "Get all nodes from SDNC using NETCONF-API",
                                             f"{self.base_url}"
                                             f"/rests/data/network-topology:network-topology/"
                                             f"topology={self.topology_id}/node={node_id}")
        try:
            node = node_object["network-topology:node"][0]
            return Node(node_id=node["node-id"],
                        host=node[NETCONF_NODE_TOPOLOGY_HOST],
                        port=node[NETCONF_NODE_TOPOLOGY_PORT],
                        username=node[NETCONF_NODE_TOPOLOGY_USERNAME],
                        password=node[NETCONF_NODE_TOPOLOGY_PASSWORD],
                        topology_id=self.topology_id)
        except KeyError:
            self._logger.error("Error. Node creation skipped.")
            return None

    def get_all_nodes(self) -> Iterable["Node"]:
        """Get all nodes of the specific topology from SDNC using NETCONF-API.

        Yields:
            : Node object
        """
        nodes_object = self.send_message_json("GET",
                                              "Get all nodes from SDNC using NETCONF-API",
                                              f"{self.base_url}/rests/data"
                                              f"/network-topology:network-topology/"
                                              f"topology={self.topology_id}"
                                              )
        nodes = nodes_object["network-topology:topology"][0]["node"]
        for node in nodes:
            try:
                yield Node(node_id=node["node-id"],
                           host=node[NETCONF_NODE_TOPOLOGY_HOST],
                           port=node[NETCONF_NODE_TOPOLOGY_PORT],
                           username=node[NETCONF_NODE_TOPOLOGY_USERNAME],
                           password=node[NETCONF_NODE_TOPOLOGY_PASSWORD],
                           topology_id=self.topology_id)
            except KeyError:
                self._logger.error("Error. Node creation skipped. KeyError")
