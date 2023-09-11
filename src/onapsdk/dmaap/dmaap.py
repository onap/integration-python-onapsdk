"""Base Dmaap event store."""
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
from typing import Dict
from onapsdk.dmaap.dmaap_service import DmaapService

ACTION = "Get events from Dmaap"
GET_HTTP_METHOD = "GET"


class Dmaap(DmaapService):
    """Dmaap library provides functions for getting events from Dmaap."""

    dmaap_url = DmaapService._url
    get_all_events_url = f"{dmaap_url}/events"
    get_all_topics_url = f"{dmaap_url}/topics"
    get_events_from_topic_url = "{}/events/{}/CG1/C1"

    @classmethod
    def get_all_events(cls,
                       basic_auth: Dict[str, str]) -> dict:
        """
        Get all events stored in Dmaap.

        Args:
           basic_auth: (Dict[str, str]) for example:{ 'username': 'bob', 'password': 'secret' }
        Returns:
            (dict) Events from Dmaap

        """
        return Dmaap.__get_events(cls.get_all_events_url, basic_auth)

    @classmethod
    def get_events_for_topic(cls,
                             topic: str,
                             basic_auth: Dict[str, str]) -> dict:
        """
        Get all events stored specific topic in Dmaap.

        Args:
            topic: (str) topic of events stored in Dmaap
            basic_auth: (Dict[str, str]) for example:{ 'username': 'bob', 'password': 'secret' }

        Returns:
          (dict) Events from Dmaap

        """
        url = cls.get_events_from_topic_url.format(cls.dmaap_url, topic)
        return Dmaap.__get_events(url, basic_auth)

    @classmethod
    def get_all_topics(cls,
                       basic_auth: Dict[str, str]) -> dict:
        """
        Get all topics stored in Dmaap.

        Args:
           basic_auth: (Dict[str, str]) for example:{ 'username': 'bob', 'password': 'secret' }

        Returns:
            (dict) Topics from Dmaap

        """
        return Dmaap.__get_events(cls.get_all_topics_url, basic_auth)['topics']

    @classmethod
    def __get_events(cls,
                     url: str,
                     basic_auth: Dict[str, str]) -> dict:
        return cls.send_message_json(
            GET_HTTP_METHOD,
            ACTION,
            url,
            basic_auth=basic_auth
        )

    @classmethod
    def post_event(cls,
                   topic: str,
                   event: str):
        """Post an event on given topic.

        Post an event on given topic by calling DMaaP REST API

        Args:
            topic: (str) topic on which to publish the event
            event: (str) event payload

        """
        cls.send_message("POST",
                         f"Publish Event via DMaaP on {topic} topic",
                         f"{cls.get_all_events_url}/{topic}",
                         data=event)
