import pathlib
from abc import ABC, abstractmethod
from typing import *


class IFileAccessor(ABC):
    @abstractmethod
    def read_file(self, file: pathlib.Path) -> bytes:
        pass

    @abstractmethod
    def write_file(self, file: pathlib.Path, data: bytes):
        pass
