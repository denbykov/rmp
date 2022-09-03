from abc import ABC, abstractmethod
from typing import *

from source.Business.Entities.Tag.Tag import *
from source.Business.Entities.Tag.ParsingProgress import *


class IParsingManager(ABC):
    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def enqueue_tag(self, tag: Tag, native_tag: Tag):
        pass

    @abstractmethod
    def enqueue_native_tag(self, tag: Tag, uid: str):
        pass

    @abstractmethod
    def get_progress(self, tag_id: int) -> Optional[Tuple[ParsingProgress, Tag]]:
        pass

    @abstractmethod
    def del_progress(self, tag_id: int):
        pass
