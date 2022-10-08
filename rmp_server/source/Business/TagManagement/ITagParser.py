from abc import ABC, abstractmethod

from source.Business.Entities.Tag.Tag import *

from typing import *


class ITagParser(ABC):
    @abstractmethod
    def parse(self, tag: Tag, data: Dict):
        pass
