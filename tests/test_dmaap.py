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
from unittest.mock import patch

from onapsdk.dmaap.dmaap import Dmaap, ACTION, GET_HTTP_METHOD

TOPIC = "fault"

DMAAP_EVENTS_URL = "http://dmaap.api.simpledemo.onap.org:3904/events"
DMAAP_EVENTS_FROM_TOPIC_URL = f"http://dmaap.api.simpledemo.onap.org:3904/events/{TOPIC}/CG1/C1"
DMAAP_RESET_EVENTS = "http://dmaap.api.simpledemo.onap.org:3904/reset"
DMAAP_GET_ALL_TOPICS = "http://dmaap.api.simpledemo.onap.org:3904/topics"
BASIC_AUTH = {'username': 'dcae@dcae.onap.org', 'password': 'demo123456!'}


@patch.object(Dmaap, "send_message_json")
def test_should_get_all_events(send_message_mock):
    Dmaap.get_all_events(BASIC_AUTH)
    verify_send_event_to_ves_called(send_message_mock, DMAAP_EVENTS_URL)

@patch.object(Dmaap, "send_message_json")
def test_should_get_events_from_topic(send_message_mock):
    Dmaap.get_events_for_topic(TOPIC, BASIC_AUTH)
    verify_send_event_to_ves_called(send_message_mock, DMAAP_EVENTS_FROM_TOPIC_URL)

@patch.object(Dmaap, "send_message_json")
def test_should_get_all_topics(send_message_mock):
    Dmaap.get_all_topics(BASIC_AUTH)
    verify_send_event_to_ves_called(send_message_mock, DMAAP_GET_ALL_TOPICS)

def verify_send_event_to_ves_called(send_message_mock, dmaap_url):
    send_message_mock.assert_called_once_with(
        GET_HTTP_METHOD, ACTION, dmaap_url,
        basic_auth=BASIC_AUTH
    )

