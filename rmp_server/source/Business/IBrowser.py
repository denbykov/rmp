from abc import ABC, abstractmethod
from typing import *


class IBrowser(ABC):
    @abstractmethod
    def get_page_content(self, url: str) -> str:
        pass

    @abstractmethod
    def locate_to_page(self, url: str):
        pass

    @abstractmethod
    def click_element(self, xpath: str, sleep_for: int = 1):
        pass

    @abstractmethod
    def get_text_of_element(self, xpath: str) -> str:
        pass
