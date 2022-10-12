from abc import ABC, abstractmethod

from source.Business.Entities.Tag.TagSource import *
from .IWebParser import IWebParser

from typing import *


class IWebParserFactory(ABC):
    @abstractmethod
    def create(self, source: TagSourceName) -> IWebParser:
        pass
