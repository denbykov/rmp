from abc import ABC, abstractmethod

from source.Business.Entities.Tag.TagSource import *
from .ITagParser import ITagParser

from typing import *


class ITagParserFactory(ABC):
    @abstractmethod
    def create(self, source: TagSourceName) -> ITagParser:
        pass
