"""Test SDNC service creation using GENERIC-RESOURCE-API."""
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
import json
from collections.abc import Iterable
from typing import Dict
from unittest import mock

from onapsdk.sdnc.topology import Topology

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
                            "netconf-master-node": "akka://opendaylight-cluster-data@onap-sdnc-0.sdnc-cluster.onap.svc.cluster.local:2550"
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
@mock.patch.object(Topology, "send_message_json")
def test_sdnc_topology_netconf_api_get_network_topology(mock_send_message_json):
    mock_send_message_json.return_value = SDNC_TOPOLOGY
    sdnc_network_topology = Topology.get_network_topology()
    assert isinstance(sdnc_network_topology, Iterable)
    sdnc_network_topology_list = list(sdnc_network_topology)
    assert len(sdnc_network_topology_list) == 1
    topology = sdnc_network_topology_list[0]
    assert isinstance(topology, Topology)
    assert topology.topology_id == SDNC_TOPOLOGY_ID
