from abc import ABC, abstractmethod
from typing import *


class IBrowser(ABC):
    @abstractmethod
    def get_page_content(self, url: str) -> str:
        pass
