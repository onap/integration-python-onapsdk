"""Base kafka module."""
#   Copyright Deutsche Telekom AG
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

from onapsdk.configuration import settings
from onapsdk.onap_service import OnapService


class KafkaService(OnapService):
    """
    A class representing a Kafka service.

    This class provides configuration parameters for connecting to Kafka,
    including bootstrap servers, security protocol, SASL mechanism, group ID,
    auto commit settings, consumer timeout, and thread sleep intervals.

    Attributes:
        bootstrap_server (str): The bootstrap server(s) for Kafka connection.
        security_protocol (str): The security protocol for Kafka connection.
        sasl_mechanism (str): The SASL mechanism for Kafka connection.
        group_id (str): The group ID for Kafka consumer.
        enable_auto_commit (bool): Whether to enable auto commit for Kafka consumer.
        auto_offset_reset (str): The auto offset reset strategy for Kafka consumer.
        consumer_timeout_ms (int): The consumer timeout in milliseconds for Kafka consumer.
        consumer_thread_sleep (int): The sleep interval in seconds for Kafka consumer thread.
    """

    bootstrap_server: str = settings.KAFKA_BOOTSTRAP_SERVERS
    security_protocol: str = settings.KAFKA_SECURITY_PROTOCOL
    sasl_mechanism: str = settings.KAFKA_SASL_MECHANISM
    group_id: str = settings.KAFKA_GROUP_ID
    enable_auto_commit: bool = settings.KAFKA_ENABLE_AUTO_COMMIT
    auto_offset_reset: str = settings.KAFKA_AUTO_OFFSET_RESET
    consumer_timeout_ms: int = settings.KAFKA_CONSUMER_TIMEOUT_MS
    consumer_thread_sleep: int = settings.KAFKA_CONSUMER_THREAD_SLEEP
