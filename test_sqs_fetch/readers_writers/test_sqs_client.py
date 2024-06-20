import unittest
from unittest.mock import patch, MagicMock
from sqs_fetch.readers_writers.sqs_client import SQSClient


class TestSQSClient(unittest.TestCase):

    def setUp(self):
        self.endpoint_url = 'http://localhost:4566'
        self.region_name = 'us-east-1'
        self.queue_name = 'test-queue'
        self.queue_url = 'http://localhost:4566/myqueue'
        self.messages = [{'MessageId': 'xabc-ux12', 'Body': 'Testing 123'}]

    def test_read_messages(self, ):
        with patch('sqs_fetch.readers_writers.sqs_client.SQSConnection') as sqs_connection:
            sqs_connection.return_value.sqs.receive_message.return_value = {'Messages': self.messages}
            sqs_connection.return_value.queue_url = self.queue_url

            sqs_client = SQSClient(self.endpoint_url, self.region_name, self.queue_name)
            received_messages = sqs_client.read_messages()

            sqs_connection.return_value.sqs.receive_message.assert_called_once_with(
                QueueUrl=self.queue_url,MaxNumberOfMessages=10,WaitTimeSeconds=20)
            self.assertEqual(received_messages, self.messages)

