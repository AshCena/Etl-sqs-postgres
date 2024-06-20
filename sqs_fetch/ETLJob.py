from typing import Dict, Any, Callable, List
import json

from readers_writers.read_client import ReadClient
from readers_writers.write_client import WriteClient
from utils.transformer import Transformer
from utils.validator import Validator


class ETLJob:

    """
    This class is the main class for ETL functionality. It will have the extract, transform, load.
    extract: read_messages
    transform: do_transform
    load: write
    """

    def __init__(self, read_client: ReadClient, write_client: WriteClient, validator: Validator):
        self.read_client = read_client
        self.write_client = write_client
        self.messages = []
        self.valid_messages = []
        self.transformed_data = []
        self.validator = validator

    def read_messages(self):
        self.messages = self.read_client.read_messages()
        return self

    def validate_messages(self) -> List[Dict[str, Any]]:
        self.valid_messages = []
        self.valid_messages = [message for message in self.messages if self.validator.validate(json.loads(message["Body"]))]
        return self.valid_messages

    def do_transform(self, transformer: Transformer, model):
        self.transformed_data = [model.from_dict(transformer.transform(message)) for message in self.valid_messages]
        return self

    def write(self):
        self.write_client.write(self.transformed_data)
        self.transformed_data = []
        return self

    def start(self, transformer: Transformer, model):
        self.read_messages()
        validated_messages = self.validate_messages()
        if validated_messages:
            self.do_transform(transformer=transformer, model=model).write()
            print("Executing Write Step")
            self.start(transformer, model)
        else:
            print("No New Messages Found")
        return self
