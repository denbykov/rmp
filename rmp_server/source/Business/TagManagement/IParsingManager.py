from abc import ABC, abstractmethod
from typing import *

from source.Business.Entities.File.FileSourceInfo import *
from source.Business.Entities.File.File import *
from source.Business.Entities.File.DownloadingProgress import *


class IDownloadingManager(ABC):
    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def enqueue_file(self, file: File, info: FileSourceInfo):
        pass

    @abstractmethod
    def get_progress(self, file_id: int) -> Optional[DownloadingProgress]:
        pass

    @abstractmethod
    def del_progress(self, file_id: int):
        pass
