from abc import ABC, abstractmethod

from source.Business.Entities.File.FileSourceInfo import *
from source.Business.Entities.File.File import *
from source.Business.Entities.File.DownloadingProgress import *

import threading


class IDownloader(ABC):
    @staticmethod
    @abstractmethod
    def download(
            file: File,
            info: FileSourceInfo,
            lock: threading.Lock,
            progress: DownloadingProgress):
        pass
