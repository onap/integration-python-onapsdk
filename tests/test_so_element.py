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
from unittest import mock

from onapsdk.so.so_element import SoElement
from onapsdk.utils.gui import GuiList

@mock.patch.object(SoElement, "send_message")
def test_get_guis(send_message_mock):
    component = SoElement()
    send_message_mock.return_value.status_code = 200
    send_message_mock.return_value.url = "http://so.api.simpledemo.onap.org:30277/"
    gui_results = component.get_guis()
    assert type(gui_results) == GuiList
    assert gui_results.guilist[0].url == send_message_mock.return_value.url
    assert gui_results.guilist[0].status == send_message_mock.return_value.status_code
