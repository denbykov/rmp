from abc import ABC, abstractmethod
from typing import *


class IRequestAgent(ABC):
    def read_json(self, url: str) -> Tuple[int, Dict[str, Any]]:
        pass

    def read_json_file(self, url: str) -> Tuple[int, Dict[str, Any]]:
        pass

    def read_file(self, url: str) -> Tuple[int, bytes]:
        pass
