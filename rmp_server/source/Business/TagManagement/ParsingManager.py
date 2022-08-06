from .IDownloadingManager import *

from .Downloaders.IDownloader import *
from .Downloaders.YTDownloader import *

import threading

import queue

import logging
import source.LoggerNames as LoggerNames

from typing import *

import copy


class DownloadingManager(IDownloadingManager):
    """Application must have only one instance of DownloadingManager!"""

    def __init__(self):
        self.logger: logging.Logger = logging.getLogger(LoggerNames.BUSINESS)
        self.queue: queue.Queue = queue.Queue()
        self.progress_lock: threading.Lock = threading.Lock()
        self.progress_storage: Dict[int, DownloadingProgress] = dict()

    def run(self) -> None:
        self.logger.info("Starting downloader")
        thread: threading.Thread = \
            threading.Thread(target=self._mainloop, args=(self,), daemon=True)
        thread.start()
        self.logger.info("Downloader loop started")

    @staticmethod
    def _mainloop(manager) -> None:
        while True:
            task: Tuple[File, FileSourceInfo] = manager.queue.get()

            try:
                downloader: IDownloader = manager._get_downloader(task[1])

                with manager.progress_lock:
                    manager.progress_storage[task[0].id] = \
                        DownloadingProgress(0, 0, FileStateName.LOADING)

                downloader.download(
                    task[0],
                    task[1],
                    manager.progress_lock,
                    manager.progress_storage[task[0].id])

            except RuntimeError:
                manager.logger.error(f"Failed to create downloader for {task[1].source}")

            except Exception as ex:
                manager.logger.error(f"Downloading error: {ex}")

            manager.queue.task_done()

    @staticmethod
    def _get_downloader(info: FileSourceInfo):
        if info.source == FileSource.YOUTUBE:
            return YTDownloader

        raise RuntimeError("Unknown file source")

    def enqueue_file(self, file: File, info: FileSourceInfo):
        try:
            self.queue.put((file, info))
        except Exception as ex:
            self.logger.error(f"Failed to add file to the downloading queue: {file.url}"
                              f"reason: {ex}")

        self.logger.info(f"File added to the downloading queue: {file.url}")

    def get_progress(self, file_id: int) -> Optional[DownloadingProgress]:
        progress: Optional[DownloadingProgress] = None

        try:
            with self.progress_lock:
                progress = copy.deepcopy(self.progress_storage[file_id])
        except KeyError:
            pass

        return progress

    def del_progress(self, file_id: int):
        with self.progress_lock:
            del self.progress_storage[file_id]
