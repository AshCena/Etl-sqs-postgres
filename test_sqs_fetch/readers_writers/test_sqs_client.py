import unittest
from unittest.mock import patch, MagicMock
# from sqs_fetch.readers_writers.sqs_client import SQSClient


class TestSQSClient(unittest.TestCase):

    def setUp(self):
        self.endpoint_url = 'http://localhost:4566'
        self.region_name = 'us-east-1'
        self.queue_name = 'test-queue'
        self.queue_url = 'http://localhost:4566/myqueue'
        self.messages = [{'MessageId': 'xabc-ux12', 'Body': 'Testing 123'}]

    def test_read_messages(self, ):
        return True

