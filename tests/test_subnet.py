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
import pytest
from onapsdk.exceptions import ParameterError

from onapsdk.so.instantiation import Subnet


def test_dhcp_subnet():
    with pytest.raises(ParameterError):
        Subnet(name="test",
               role="test",
               start_address="192.168.8.0",
               gateway_address="192.168.8.1",
               dhcp_enabled="sss"
        )
    with pytest.raises(ParameterError):
        Subnet(name="test",
               role="test",
               start_address="192.168.8.0",
               gateway_address="192.168.8.1",
               dhcp_enabled="Y"
        )
    subnet = Subnet(name="test",
                    role="test",
                    start_address="192.168.8.0",
                    gateway_address="192.168.8.1",
                    dhcp_enabled="Y",
                    dhcp_start_address="10.8.1.0",
                    dhcp_end_address="10.8.1.1"
    )
    assert subnet.name == "test"
    assert subnet.role == "test"
    assert subnet.start_address == "192.168.8.0"
    assert subnet.gateway_address == "192.168.8.1"
    assert subnet.dhcp_enabled == "Y"
    assert subnet.dhcp_start_address == "10.8.1.0"
    assert subnet.dhcp_end_address == "10.8.1.1"
