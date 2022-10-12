from abc import ABC, abstractmethod
from typing import *


class IRequestAgent(ABC):
    def read_json(self, url: str) -> Tuple[int, Dict[str, Any]]:
        pass

    def read_json_file(
            self,
            url: str,
            token: Optional[str] = None) -> Tuple[int, Dict[str, Any]]:
        pass

    def read_file(self, url: str) -> Tuple[int, bytes]:
        pass

    def post_and_read_json(
            self,
            url: str,
            headers: Optional[Dict] = None,
            data: Optional[Dict] = None) \
            -> Tuple[int, Dict]:
        pass
