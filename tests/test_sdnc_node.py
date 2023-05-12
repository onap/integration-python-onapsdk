"""Test SDNC node creation using NETCONF-API."""
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
from unittest import mock

from onapsdk.sdnc.topology import Node

SDNC_NODE = {
    "network-topology:node": [
        {
            "node-id": "test-node",
            "netconf-node-topology:host": "100.70.0.5",
            "netconf-node-topology:port": 830,
            "netconf-node-topology:keepalive-delay": 100,
            "netconf-node-topology:tcp-only": False,
            "netconf-node-topology:username": "root",
            "netconf-node-topology:password": "password"
        }
    ]
}

SDNC_TOPOLOGY_ID = "topology-netconf"


def test_sdnc_netconf_api_node_init():
    node = Node(node_id=SDNC_NODE["network-topology:node"][0]["node-id"],
                host=SDNC_NODE["network-topology:node"][0]["netconf-node-topology:host"],
                port=SDNC_NODE["network-topology:node"][0]["netconf-node-topology:port"],
                username=SDNC_NODE["network-topology:node"][0]["netconf-node-topology:username"],
                password=SDNC_NODE["network-topology:node"][0]["netconf-node-topology:password"],
                )
    assert type(node.node_id) is str


@mock.patch.object(Node, "send_message")
def test_sdnc_netconf_api_node_create(mock_send_message):
    node = Node(node_id="test-node-02",
                host="100.70.0.102",
                port=830,
                username="admin",
                password="2345",
                topology_id="topology-netconf"
                )
    node.create()

    mock_send_message.assert_called_once()
    method, description, url = mock_send_message.call_args[0]
    assert method == "POST"
    assert description == "Add a node element into the topology at SDNC using NETCONF-API"
    assert url == (f"{Node.base_url}/rests/data/"
                   f"network-topology:network-topology/topology={node.topology_id}")


@mock.patch.object(Node, "send_message")
def test_sdnc_netconf_api_node_delete(mock_send_message):
    node = Node(node_id="test-node-02",
                host="100.70.0.102",
                port=830,
                username="admin",
                password="2345",
                topology_id="topology-netconf"
                )
    node.delete()

    mock_send_message.assert_called_once()
    method, description, url = mock_send_message.call_args[0]
    assert method == "DELETE"
    assert description == "Delete a Node element from the topology using NETCONF-API"
    assert url == (f"{Node.base_url}/rests/data/"
                   f"network-topology:network-topology/topology={node.topology_id}"
                   f"/node={node.node_id}")


@mock.patch.object(Node, "send_message")
def test_sdnc_netconf_api_node_update(mock_send_message):
    node = Node(node_id="test-node-02",
                host="100.70.0.102",
                port=830,
                username="admin",
                password="2345",
                topology_id="topology-netconf"
                )
    node.update()

    mock_send_message.assert_called_once()
    method, description, url = mock_send_message.call_args[0]
    assert method == "PUT"
    assert description == "Add a Node element into the topology using NETCONF-API"
    assert url == (f"{Node.base_url}/rests/data/"
                   f"network-topology:network-topology/topology={node.topology_id}"
                   f"/node={node.node_id}")
