"""Test A&AI Element."""
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
from unittest import mock

from onapsdk.aai.aai_element import AaiResource, Relationship
from onapsdk.exceptions import RequestError, ResourceNotFound, RelationshipNotFound
from onapsdk.utils.gui import GuiList

@mock.patch.object(AaiResource, "send_message_json")
@mock.patch.object(AaiResource, "url")
def test_relationship_not_found(mock_send, mock_url):

    aai_element = AaiResource()
    mock_url.return_value = "http://my.url/"

    mock_send.side_effect = ResourceNotFound

    aai_element.send_message_json = mock_send

    with pytest.raises(ResourceNotFound) as exc:
        list(aai_element.relationships)
    assert exc.type == RelationshipNotFound

    mock_send.assert_called_once()


def test_relationship_get_relationship_data():
    r = Relationship(
        related_to="test",
        related_link="test",
        relationship_data=[{
            "relationship-key": "test",
            "relationship-value": "test"
        }]
    )
    assert r.get_relationship_data("invalid key") is None
    assert r.get_relationship_data("test") == "test"

@mock.patch.object(AaiResource, "send_message")
def test_get_guis(send_message_mock):
    component = AaiResource()
    send_message_mock.return_value.status_code = 200
    send_message_mock.return_value.url = "https://aai.api.sparky.simpledemo.onap.org:30220/services/aai/webapp/index.html#/browse"
    gui_results = component.get_guis()
    assert type(gui_results) == GuiList
    assert gui_results.guilist[0].url == send_message_mock.return_value.url
    assert gui_results.guilist[0].status == send_message_mock.return_value.status_code
