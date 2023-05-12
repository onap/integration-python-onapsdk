"""Test SDNC node creation using NETCONF-API."""
#   Copyright 2023 Orange, Deutsche Telekom AG
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
import json
from collections.abc import Iterable
from typing import Dict
from unittest import mock

from onapsdk.sdnc.topology import Topology, Node

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

@mock.patch.object(Node, "send_message")
def test_sdnc_topology_netconf_api_create(mock_send_message):
    node = Node(SDNC_TOPOLOGY_ID,
                SDNC_NODE["network-topology:node"][0]["node-id"]
                )
    node.create()

    mock_send_message.assert_called_once()
    method, description, url = mock_send_message.call_args[0]
    assert method == "POST"
    assert description == "Create a node using NETCONF-API"
    assert url == (f"{Node.base_url}/rests/data/"
                   f"network-topology:network-topology/topology=topology-netconf")

@mock.patch.object(Node, "send_message_json")
def test_sdnc_topology_netconf_api_get(mock_send_message_json):
    mock_send_message_json.return_value = SDNC_NODE
    node = Node(SDNC_TOPOLOGY_ID,
                SDNC_NODE["network-topology:node"][0]["node-id"]
                )
    node_get = node.get()
    assert isinstance(node_get, Iterable)
    node_instance = next(node_get)
    assert isinstance(node_instance, Node)
    assert node_instance.node_id == "test-node"

@mock.patch.object(Node, "send_message")
def test_sdnc_topology_netconf_api_delete(mock_send_message):
    node = Node(SDNC_TOPOLOGY_ID,
                SDNC_NODE["network-topology:node"][0]["node-id"]
                )
    node.delete()

    mock_send_message.assert_called_once()
    method, description, url = mock_send_message.call_args[0]
    assert method == "DELETE"
    assert description == "DELETE a node using NETCONF-API"
    assert url == (f"{Node.base_url}/rests/data/"
                   "network-topology:network-topology/topology=topology-netconf/"
                   "node=test-node")