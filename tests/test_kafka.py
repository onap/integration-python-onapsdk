import unittest
from unittest.mock import patch

from onapsdk.kafka.onap_kafka import get_events_for_topic, publish_event_on_topic


class TestConsumer(unittest.TestCase):

    @patch('onapsdk.kafka.onap_kafka.KafkaConsumer')
    def test_onap_consumer(self, mock_KafkaConsumer):
        # Prepare test data
        username = "test_user"
        password = "test_password"
        topic = "test_topic"

        # Configure the mock KafkaConsumer
        mock_consumer_instance = mock_KafkaConsumer.return_value
        mock_consumer_instance.subscribe.return_value = None

        # Run the consumer
        record_queue = get_events_for_topic(username, password, topic, None)

        # Check if Consumer is called with the correct arguments
        mock_KafkaConsumer.assert_called_once_with(
            bootstrap_servers='onap-strimzi-kafka-bootstrap',
            security_protocol='SASL_PLAINTEXT',
            sasl_mechanism='SCRAM-SHA-512',
            sasl_plain_username=username,
            sasl_plain_password=password,
            enable_auto_commit=True,
            auto_offset_reset='EARLIEST',
            consumer_timeout_ms=1000,
            group_id='consumer3'
        )
        print(record_queue)
        # Check if Consumer's subscribe method is called with the correct arguments
        mock_consumer_instance.subscribe.assert_called_once_with([topic])

        self.assertIsNotNone(record_queue)


class TestProducer(unittest.TestCase):

    @patch('onapsdk.kafka.onap_kafka.KafkaProducer')
    def test_onap_producer(self, mock_KafkaProducer):
        # Prepare test data
        username = "test_user"
        password = "test_password"
        topic = "test_topic1"
        data = "test_data"

        # Run the producer
        publish_event_on_topic(username, password, data, topic)

        # Check if KafkaProducer is called with the correct arguments
        mock_KafkaProducer.assert_called_once_with(
            bootstrap_servers='onap-strimzi-kafka-bootstrap',
            security_protocol='SASL_PLAINTEXT',
            sasl_mechanism='SCRAM-SHA-512',
            sasl_plain_username=username,
            sasl_plain_password=password
        )


if __name__ == "__main__":
    unittest.main()