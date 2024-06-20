from typing import Dict, List, Any

from .validator import Validator


class SchemaValidator(Validator):
    def __init__(self, schema: List[str]):
        self.schema = schema

    def validate(self, message: Dict[str, Any]) -> bool:
        return all(key in message for key in self.schema)

