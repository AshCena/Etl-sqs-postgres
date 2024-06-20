import unittest
from unittest.mock import patch, MagicMock
from sqs_fetch.connections.sqs_connection import SQSConnection


class TestSQSConnection(unittest.TestCase):

    def setUp(self):
        self.endpoint_url = 'http://localhost:4566'
        self.region_name = 'us-east-1'
        self.queue_name = 'test-queue'
        self.queue_url = 'http://localhost:4566/queue'

    def test_init_sqs_connection(self):
        with patch('sqs_fetch.connections.sqs_connection.boto3.client') as boto_client:
            sqs_client = MagicMock()
            boto_client.return_value = sqs_client
            sqs_client.get_queue_url.return_value = {'QueueUrl': self.queue_url}

            sqs_connection = SQSConnection(self.endpoint_url, self.region_name, self.queue_name)

            self.assertEqual(sqs_connection.queue_url, self.queue_url)
            boto_client.assert_called_once_with('sqs', region_name=self.region_name,
                                                endpoint_url=self.endpoint_url)
            sqs_client.get_queue_url.assert_called_once_with(QueueName=self.queue_name)


