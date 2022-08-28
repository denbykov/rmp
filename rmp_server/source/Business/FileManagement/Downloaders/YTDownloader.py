from .IDownloader import *

from source.Presentation.Formatters.URLFormatter import *

import logging
import source.LoggerNames as LoggerNames

import yt_dlp


class Logger:
    def __init__(self):
        self.logger: logging.Logger = logging.getLogger(LoggerNames.BUSINESS)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)

    def warning(self, msg):
        self.logger.warning(msg)


class ProgressHook:
    def __init__(self, lock: threading.Lock, progress: DownloadingProgress):
        self.lock: threading.Lock = lock
        self.progress: DownloadingProgress = progress

    def __call__(self, progress):
        self._update_progress(progress)

    def _update_progress(self, progress: dict):
        if progress['status'] == 'finished':
            with self.lock:
                self.progress.state = FileStateName.CONVERTING
        elif progress['status'] == 'downloading':
            with self.lock:
                self.progress.state = FileStateName.LOADING
                try:
                    total_bytes = None
                    if progress.get("total_bytes_estimate") is not None:
                        total_bytes = progress.get("total_bytes_estimate")
                    if progress.get("total_bytes") is not None:
                        total_bytes = progress.get("total_bytes")

                    if total_bytes is not None:
                        self.progress.percent = \
                            progress["downloaded_bytes"] / total_bytes * 100

                    self.progress.speed = progress["speed"] / 1000
                except TypeError:
                    pass
                except KeyError:
                    pass
        else:
            logger: logging.Logger = logging.getLogger(LoggerNames.BUSINESS)
            logger.error(
                f"YTDownloader satus hook ist unable to process"
                f" status {progress['status']}")


class YTDownloader(IDownloader):
    @staticmethod
    @abstractmethod
    def download(
            file: File,
            info: FileSourceInfo,
            lock: threading.Lock,
            progress: DownloadingProgress):
        ydl_opts = {
            'outtmpl': str(file.path),
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger': Logger(),
            'progress_hooks': [ProgressHook(lock, progress)],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([URLFormatter.format(info)])

        YTDownloader._update_progress(lock, progress)

    @staticmethod
    def _update_progress(
            lock: threading.Lock,
            progress: DownloadingProgress):
        with lock:
            if progress.state == FileStateName.CONVERTING or \
               progress.state == FileStateName.LOADING:
                progress.state = FileStateName.READY
