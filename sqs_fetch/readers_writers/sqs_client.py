from typing import List, Dict, Any

from connections.sqs_connection import SQSConnection
from .client_registery import client_registry
from .read_client import ReadClient


class SQSClient(ReadClient):

    """
    This class helps instantiate the Read class which will help in the Extract step for ETL
    """

    def __init__(self, endpoint_url: str, region_name: str, queue_name: str):
        self.sqs_connection = SQSConnection(endpoint_url, region_name, queue_name)

    def read_messages(self) -> List[Dict[str, Any]]:
        response = self.sqs_connection.sqs.receive_message(
            QueueUrl=self.sqs_connection.queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=20
        )
        return response.get('Messages', [])


client_registry.register('sqs', SQSClient)
