"""Test SDNC topology creation using NETCONF-API."""
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
from collections.abc import Iterable
from unittest import mock

from onapsdk.sdnc.topology import Topology, Node

SDNC_TOPOLOGY_GET_NODE = {
    "network-topology:node": [
        {
            "node-id": "TEST",
            "netconf-node-topology:sleep-factor": "1.5",
            "netconf-node-topology:host": "10.1.1.41",
            "netconf-node-topology:reconnect-on-changed-schema": False,
            "netconf-node-topology:between-attempts-timeout-millis": 2000,
            "netconf-node-topology:connection-status": "connected",
            "netconf-node-topology:max-connection-attempts": 0,
            "netconf-node-topology:username": "admin",
            "netconf-node-topology:password": "admin",
            "netconf-node-topology:connection-timeout-millis": 20000,
            "netconf-node-topology:port": 32767,
            "netconf-node-topology:tcp-only": False,
            "netconf-node-topology:keepalive-delay": 120
        }
    ]
}
SDNC_TOPOLOGY_GET_NODE_KEY_ERROR = {
    "network-topology:node": [
        {
            "node-id": "TEST",
            "netconf-node-topology:host": "10.1.1.41",
            "netconf-node-topology:username": "admin",
            "netconf-node-topology:password": "admin"
        }
    ]
}

SDNC_TOPOLOGY_GET_ALL_NODES_KEY_ERROR = {
    "network-topology:topology": [
        {
            "topology-id": "topology-netconf",
            "node": [
                {
                    "node-id": "TEST1",
                    "netconf-node-topology:host": "10.1.1.41",
                    "netconf-node-topology:username": "admin",
                    "netconf-node-topology:password": "admin",
                },
                {
                    "node-id": "TEST2",
                    "netconf-node-topology:port": 830,
                    "netconf-node-topology:username": "root",
                    "netconf-node-topology:password": "password",
                    "netconf-node-topology:host": "100.70.0.53"
                }
            ]
        }
    ]
}

SDNC_TOPOLOGY_WITHOUT_NODES_GET_ALL = {
    "network-topology:network-topology": {
        "topology": [
            {
                "topology-id": "topology-netconf",
            }
        ]
    }
}

SDNC_TOPOLOGY_WITHOUT_NODES_GET = {
    "network-topology:topology": [
        {
            "topology-id": "topology-netconf",
        }
    ]
}

SDNC_TOPOLOGY_GET_ALL_NODES = {
    "network-topology:topology": [
        {
            "topology-id": "topology-netconf",
            "node": [
                {
                    "node-id": "TEST",
                    "netconf-node-topology:host": "10.1.1.41",
                    "netconf-node-topology:username": "admin",
                    "netconf-node-topology:password": "admin",
                    "netconf-node-topology:port": 32767
                }
            ]
        }
    ]
}
SDNC_TOPOLOGY = {
    "network-topology:network-topology": {
        "topology": [
            {
                "topology-id": "topology-netconf",
                "node": [
                    {
                        "node-id": "MAAS",
                        "netconf-node-topology:sleep-factor": "1.5",
                        "netconf-node-topology:host": "10.32.32.32",
                        "netconf-node-topology:reconnect-on-changed-schema": False,
                        "netconf-node-topology:clustered-connection-status": {
                            "netconf-master-node": "test"
                        },
                        "netconf-node-topology:between-attempts-timeout-millis": 2000,
                        "netconf-node-topology:connection-status": "connected",
                        "netconf-node-topology:max-connection-attempts": 0,
                        "netconf-node-topology:username": "admin",
                        "netconf-node-topology:password": "admin",
                        "netconf-node-topology:available-capabilities": {
                            "available-capability": [
                                {
                                    "capability": "urn:ietf:params:netconf:base:1.1",
                                    "capability-origin": "device-advertised"
                                }
                            ]
                        },
                        "netconf-node-topology:connection-timeout-millis": 10000,
                        "netconf-node-topology:port": 32767,
                        "netconf-node-topology:tcp-only": False,
                        "netconf-node-topology:keepalive-delay": 120
                    }
                ]
            }
        ]
    }
}
SDNC_TOPOLOGY_ID = "topology-netconf"
SDNC_NODE = {
    "network-topology:node": [
        {
            "node-id": "test-node-fff",
            "netconf-node-topology:host": "100.70.0.5",
            "netconf-node-topology:port": 830,
            "netconf-node-topology:keepalive-delay": 100,
            "netconf-node-topology:tcp-only": False,
            "netconf-node-topology:username": "root",
            "netconf-node-topology:password": "password"
        }
    ]
}

SDNC_NODE_ID = "test-node-fff"


@mock.patch.object(Topology, "send_message_json")
def test_sdnc_netconf_api_topology_get_all(mock_send_message_json):
    mock_send_message_json.return_value = SDNC_TOPOLOGY
    topology_iterable = Topology.get_all()
    assert isinstance(topology_iterable, Iterable)
    topology_list = list(topology_iterable)
    assert len(topology_list) == 1
    topology = topology_list[0]
    assert isinstance(topology, Topology)
    assert topology.topology_id == SDNC_TOPOLOGY_ID


@mock.patch.object(Topology, "send_message_json")
def test_sdnc_netconf_api_topology_get(mock_send_message_json):
    mock_send_message_json.return_value = SDNC_TOPOLOGY_GET_ALL_NODES
    topology = Topology()
    topology_new = Topology.get(topology.topology_id)
    assert isinstance(topology_new, Topology)


@mock.patch.object(Topology, "send_message_json")
def test_sdnc_netconf_api_topology_get_all_nodes(mock_send_message_json):
    mock_send_message_json.return_value = SDNC_TOPOLOGY_GET_ALL_NODES
    topology = Topology()
    nodes = topology.get_all_nodes()
    assert isinstance(nodes, Iterable)
    node_list = list(nodes)
    assert len(node_list) == 1


@mock.patch.object(Topology, "send_message_json")
def test_sdnc_netconf_api_topology_get_node(mock_send_message_json):
    mock_send_message_json.return_value = SDNC_TOPOLOGY_GET_NODE
    topology = Topology()
    node = topology.get_node("TEST")
    assert isinstance(node, Node)
    assert node.node_id == "TEST"

@mock.patch.object(Topology, "send_message_json")
def test_sdnc_netconf_api_topology_get_all_key_error(mock_send_message_json):
    mock_send_message_json.return_value = SDNC_TOPOLOGY_WITHOUT_NODES_GET_ALL
    topology_iterable = Topology.get_all()
    assert isinstance(topology_iterable, Iterable)
    topology_list = list(topology_iterable)
    assert len(topology_list) == 1
    topology = topology_list[0]
    assert topology.nodes is None

@mock.patch.object(Topology, "send_message_json")
def test_sdnc_netconf_api_topology_get_key_error(mock_send_message_json):
    mock_send_message_json.return_value = SDNC_TOPOLOGY_WITHOUT_NODES_GET
    topology = Topology.get(SDNC_TOPOLOGY_ID)
    assert isinstance(topology, Topology)
    assert topology.nodes is None

@mock.patch.object(Topology, "send_message_json")
def test_sdnc_netconf_api_topology_get_all_nodes_key_error(mock_send_message_json):
    mock_send_message_json.return_value = SDNC_TOPOLOGY_GET_ALL_NODES_KEY_ERROR
    topology = Topology()
    nodes = topology.get_all_nodes()
    assert isinstance(nodes, Iterable)
    try:
        list(nodes)
    except Exception as e:
        assert e is KeyError

@mock.patch.object(Topology, "send_message_json")
def test_sdnc_netconf_api_topology_get_node_key_error(mock_send_message_json):
    mock_send_message_json.return_value = SDNC_TOPOLOGY_GET_NODE_KEY_ERROR
    topology = Topology()
    try:
        topology.get_node("TEST")
    except Exception as e:
        assert e is KeyError
