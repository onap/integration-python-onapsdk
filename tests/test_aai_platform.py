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

from onapsdk.aai.business.platform import Platform

PLATFORMS = {
    "platform": [
        {
            "platform-name": "test-name",
            "resource-version": "1234"
        },
        {
            "platform-name": "test-name2",
            "resource-version": "4321"
        }
    ]
}

COUNT = {
    "results": [
        {
            "platform": 1
        }
    ]
}


@mock.patch("onapsdk.aai.business.platform.Platform.send_message_json")
def test_platform_get_all(mock_send_message_json):
    mock_send_message_json.return_value = {}
    assert len(list(Platform.get_all())) == 0

    mock_send_message_json.return_value = PLATFORMS
    platforms = list(Platform.get_all())
    assert len(platforms) == 2
    lob1, lob2 = platforms
    assert lob1.name == "test-name"
    assert lob1.resource_version == "1234"
    assert lob2.name == "test-name2"
    assert lob2.resource_version == "4321"


@mock.patch("onapsdk.aai.business.platform.Platform.send_message_json")
def test_platform_get_by_name(mock_send):
    Platform.get_by_name(name="test-name")
    mock_send.assert_called_once_with("GET",
                                      "Get test-name platform",
                                      "https://aai.api.sparky.simpledemo.onap.org:30233/aai/v27/business/platforms/platform/test-name")


@mock.patch("onapsdk.aai.business.platform.Platform.send_message")
@mock.patch("onapsdk.aai.business.platform.Platform.get_by_name")
def test_platform_create(_, mock_send):
    Platform.create(name="test-name")
    mock_send.assert_called_once_with("PUT",
                                      "Declare A&AI platform",
                                      "https://aai.api.sparky.simpledemo.onap.org:30233/aai/v27/business/platforms/platform/test-name",
                                      data='{\n    "platform-name": "test-name"\n}')


@mock.patch("onapsdk.aai.business.platform.Platform.send_message_json")
def test_line_of_business_count(mock_send_message_json):
    mock_send_message_json.return_value = COUNT
    assert Platform.count() == 1


def test_platform_url():
    platform = Platform(name="test-platform", resource_version="123")
    assert platform.name in platform.url


@mock.patch.object(Platform, "send_message")
def test_platform_delete(mock_send_message):
    platform = Platform(name="test_platform",
                             resource_version="12345")
    platform.delete()
    mock_send_message.assert_called_once_with(
        "DELETE",
        "Delete platform",
        f"{platform.url}?resource-version={platform.resource_version}"
    )
