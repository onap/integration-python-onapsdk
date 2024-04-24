"""Base Kafka event store."""
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
import threading
import time
from queue import Queue

from kafka import KafkaConsumer
from kafka import KafkaProducer
from onapsdk.kafka.onap_kafka_service import KafkaService


class Consumer(threading.Thread):
    """
    A class representing a Kafka consumer.

    This class provides functionality to consume messages from a Kafka topic
    and store them in a queue for processing.

    Attributes:
        username (str): The username for Kafka authentication.
        password (str): The password for Kafka authentication.
        topic (str): The Kafka topic to subscribe to.
        record_queue (Queue): The queue to store consumed records.
    """

    def __init__(self, username, password, topic, record_queue):
        """
        Initialize the Consumer instance.

        Args:
            username (str): The username for Kafka authentication.
            password (str): The password for Kafka authentication.
            topic (str): The Kafka topic to subscribe to.
            record_queue (Queue): The queue to store consumed records.
        """
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()
        self.username = username
        self.password = password
        self.topic = topic
        self.record_queue = record_queue

    def stop(self):
        """
        Stop the consumer thread.

        This method sets the stop event to stop the consumer thread.
        """
        self.stop_event.set()

    def run(self):
        """
        Start consuming messages from the Kafka topic.

        This method starts consuming messages from the Kafka topic
        and puts them into the record queue for processing.
        """
        consumer_kwargs = {
            'bootstrap_servers': KafkaService.bootstrap_server,
            'security_protocol': KafkaService.security_protocol,
            'sasl_mechanism': KafkaService.sasl_mechanism,
            'sasl_plain_username': self.username,
            'sasl_plain_password': self.password,
            'enable_auto_commit': KafkaService.enable_auto_commit,
            'auto_offset_reset': KafkaService.auto_offset_reset,
            'consumer_timeout_ms': KafkaService.consumer_timeout_ms,
            'group_id': KafkaService.group_id
        }

        consumer = KafkaConsumer(**consumer_kwargs)

        consumer.subscribe([self.topic])

        while not self.stop_event.is_set():
            for message in consumer:
                self.record_queue.put(message.value)
                if self.stop_event.is_set():
                    break

        consumer.close()


def get_events_for_topic(username, password, topic, consumer_group=None):
    """
    Run the Kafka consumer with the provided parameters.

    Args:
        username (str): The username for Kafka authentication.
        password (str): The password for Kafka authentication.
        topic (str): The Kafka topic to subscribe to.
        consumer_group (str, optional): The consumer group ID. Defaults to None.

    Returns:
        list: A list of consumed records from the Kafka topic.
    """
    if consumer_group is not None:
        KafkaService.group_id = consumer_group

    record_queue = Queue()
    consumer = Consumer(username, password, topic, record_queue)
    consumer.start()
    time.sleep(KafkaService.consumer_thread_sleep)
    consumer.stop()
    consumer.join()

    # Collect records from the queue
    consumer_records = []
    while not record_queue.empty():
        consumer_records.append(record_queue.get())

    return consumer_records


def publish_event_on_topic(username, password, data, topic):
    """
    Run the Kafka producer with the provided parameters.

    Args:
        username (str): The username for Kafka authentication.
        password (str): The password for Kafka authentication.
        data (str): The data/message to be sent.
        topic (str): The Kafka topic to send messages to.
    """
    producer = KafkaProducer(bootstrap_servers=KafkaService.bootstrap_server,
                             security_protocol=KafkaService.security_protocol,
                             sasl_mechanism=KafkaService.sasl_mechanism,
                             sasl_plain_username=username,
                             sasl_plain_password=password)
    producer.send(topic, data)
    producer.close()
