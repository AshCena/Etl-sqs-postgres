from abc import ABC, abstractmethod
from typing import Dict, List, Any


class Validator(ABC):
    @abstractmethod
    def validate(self, message: Dict[str, Any]) -> bool:
        pass
