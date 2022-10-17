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

from onapsdk.msb.esr import ESR, MSB


def test_esr():
    esr = ESR()
    assert esr.base_url == f"{MSB.base_url}/api/aai-esr-server/v1/vims"


@mock.patch.object(ESR, "send_message")
def test_est_register_vim(mock_esr_send_message):
    ESR.register_vim(
        "test_cloud_owner",
        "test_cloud_region_id",
        "test_cloud_type",
        "test_cloud_region_version",
        "test_auth_info_cloud_domain",
        "test_auth_info_username",
        "test_auth_info_password",
        "test_auth_info_url"
    )
    mock_esr_send_message.assert_called_once()
    method, _, url = mock_esr_send_message.call_args[0]
    assert method == "POST"
    assert url == ESR.base_url
