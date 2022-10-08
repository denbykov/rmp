from abc import ABC, abstractmethod

from source.Business.Entities.Tag.Tag import *

from typing import *

from source.Business.Entities.TagParsingResult import TagParsingResult


class ITagParser(ABC):
    @abstractmethod
    def parse(self, tag: Tag, data: Dict) -> TagParsingResult:
        pass
