import boto3
import os

os.environ["AWS_ACCESS_KEY_ID"] = "this is needed for boto3 to function"
os.environ["AWS_SECRET_ACCESS_KEY"] = "this is needed for boto3 to function"


class SQSConnection:
    """
    This class initializes the connection to the SQS queue.
    """

    def __init__(self, endpoint_url: str, region_name: str, queue_name: str):
        self.sqs = boto3.client('sqs', region_name=region_name, endpoint_url=endpoint_url)
        self.queue_url = self.sqs.get_queue_url(QueueName=queue_name)['QueueUrl']
