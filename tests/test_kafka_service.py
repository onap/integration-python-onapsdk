import unittest
from unittest.mock import patch

from onapsdk.kafka.onap_kafka_service import KafkaService


class TestKafkaService(unittest.TestCase):

    @patch('onapsdk.kafka.onap_kafka_service.settings')
    def test_kafka_attributes_set_from_settings(self, mock_settings):
        # Mock settings values
        mock_settings.KAFKA_BOOTSTRAP_SERVERS = 'onap-strimzi-kafka-bootstrap'
        mock_settings.KAFKA_SECURITY_PROTOCOL = 'SASL_PLAINTEXT'
        mock_settings.KAFKA_SASL_MECHANISM = 'SCRAM-SHA-512'
        mock_settings.KAFKA_GROUP_ID = 'consumer3'
        mock_settings.KAFKA_ENABLE_AUTO_COMMIT = True
        mock_settings.KAFKA_AUTO_OFFSET_RESET = 'EARLIEST'
        mock_settings.KAFKA_CONSUMER_TIMEOUT_MS = 1000
        mock_settings.KAFKA_CONSUMER_THREAD_SLEEP = 10

        kafka_service = KafkaService

        # Verify attributes are correctly set
        self.assertEqual(kafka_service.bootstrap_server, 'onap-strimzi-kafka-bootstrap')
        self.assertEqual(kafka_service.security_protocol, 'SASL_PLAINTEXT')
        self.assertEqual(kafka_service.sasl_mechanism, 'SCRAM-SHA-512')
        self.assertEqual(kafka_service.group_id, 'consumer3')
        self.assertTrue(kafka_service.enable_auto_commit)
        self.assertEqual(kafka_service.auto_offset_reset, 'EARLIEST')
        self.assertEqual(kafka_service.consumer_timeout_ms, 1000)
        self.assertEqual(kafka_service.consumer_thread_sleep, 10)


if __name__ == "__main__":
    unittest.main()
