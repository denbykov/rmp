from abc import ABC, abstractmethod

from source.Business.Entities.Tag.Tag import *
from source.Business.Entities.Tag.ParsingProgress import *

import threading

from typing import *


class IParsingDirector(ABC):
    @abstractmethod
    def parse(
            self,
            tag: Tag,
            primary_data: Union[str, Tag],
            lock: threading.Lock,
            progress: ParsingProgress) -> Tag:
        pass
