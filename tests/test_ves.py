#   Copyright 2022 Orange, Deutsche Telekom AG, Nokia
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
from unittest.mock import patch
import json

from onapsdk.ves.ves import Ves, ACTION, POST_HTTP_METHOD

VERSION = "v7"

VES_URL = f"http://ves.api.simpledemo.onap.org:30417/eventListener/{VERSION}"
VES_BATCH_URL = f"http://ves.api.simpledemo.onap.org:30417/eventListener/{VERSION}/eventBatch"

TEST_EVENT = '{"event": {"test": "val"}}'
BASIC_AUTH = {'username': 'dcae@dcae.onap.org', 'password': 'demo123456!'}


@patch.object(Ves, "send_message")
def test_should_send_event_to_ves_service(send_message_mock):
    # given

    # when
    Ves.send_event(VERSION, TEST_EVENT, BASIC_AUTH)

    # then
    verify_that_event_was_send_to_ves(TEST_EVENT, send_message_mock, VES_URL)


@patch.object(Ves, "send_message")
def test_should_send_event_batch_to_ves_service(send_message_mock):
    # given

    # when
    Ves.send_batch_event(VERSION, TEST_EVENT, BASIC_AUTH)

    # then
    verify_that_event_was_send_to_ves(TEST_EVENT, send_message_mock, VES_BATCH_URL)


def verify_that_event_was_send_to_ves(expected_event, send_message_mock, ves_url):
    send_message_mock.assert_called_once_with(
        POST_HTTP_METHOD, ACTION, ves_url,
        basic_auth=BASIC_AUTH,
        json=json.loads(expected_event)
    )
    send_message_mock.return_value = None
