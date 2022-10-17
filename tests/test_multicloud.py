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
from unittest import mock

from onapsdk.msb.multicloud import Multicloud


@mock.patch.object(Multicloud, "send_message")
def test_multicloud_register(mock_send_message):
    Multicloud.register_vim(cloud_owner="test_cloud_owner",
                            cloud_region_id="test_cloud_region")
    mock_send_message.assert_called_once()
    method, description, url = mock_send_message.call_args[0]
    assert method == "POST"
    assert description == "Register VIM instance to ONAP"
    assert url == f"{Multicloud.base_url}/test_cloud_owner/test_cloud_region/registry"


@mock.patch.object(Multicloud, "send_message")
def test_multicloud_unregister(mock_send_message):
    Multicloud.unregister_vim(cloud_owner="test_cloud_owner",
                              cloud_region_id="test_cloud_region")
    mock_send_message.assert_called_once()
    method, description, url = mock_send_message.call_args[0]
    assert method == "DELETE"
    assert description == "Unregister VIM instance from ONAP"
    assert url == f"{Multicloud.base_url}/test_cloud_owner/test_cloud_region"
