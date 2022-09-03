from .IParsingManager import *
from .IWebParserFactory import *

import threading

import queue

import logging
import source.LoggerNames as LoggerNames

from typing import *

import copy


class ParsingManager(IParsingManager):
    """Application must have only one instance of DownloadingManager!"""

    def __init__(self, parser_factory: IWebParserFactory):
        self.logger: logging.Logger = logging.getLogger(LoggerNames.BUSINESS)
        self.queue: queue.Queue = queue.Queue()
        self.progress_lock: threading.Lock = threading.Lock()
        self.active_tags_storage: Dict[int, Tuple[ParsingProgress, Tag]] = dict()
        self.parser_factory: IWebParserFactory = parser_factory

    def run(self) -> None:
        self.logger.info("Starting parsing manager")
        thread: threading.Thread = \
            threading.Thread(target=self._mainloop, args=(self,), daemon=True)
        thread.start()
        self.logger.info("Parsing manager loop started")

    @staticmethod
    def _mainloop(manager) -> None:
        while True:
            task: Tuple[Tag, Union[str, Tag]] = manager.queue.get()
            tag = task[0]
            primary_data = task[1]

            try:
                parser: IWebParser = \
                    manager.parser_factory.create_parser(tag.source.name)

                with manager.progress_lock:
                    manager.active_tags_storage[tag.id] = \
                        (ParsingProgress(TagStateName.PARSING), tag)

                parser.parse(
                    tag,
                    primary_data,
                    manager.progress_lock,
                    manager.active_tags_storage[tag.id][0])

            except RuntimeError:
                manager.logger.error(
                    f"Failed to create parser for tag with id: {tag.id}")

            except Exception as ex:
                manager.logger.error(f"Parsing error: {ex}")

            manager.queue.task_done()

    def enqueue_tag(self, tag: Tag, native_tag: Tag):
        try:
            self.queue.put((tag, native_tag))
        except Exception as ex:
            self.logger.error(
                f"Failed to add tag to the parsing queue: {tag.id}"
                f"reason: {ex}")

        self.logger.info(f"Tag added to the parsing queue: {tag.id}")

    def enqueue_native_tag(self, tag: Tag, uid: str):
        try:
            self.queue.put((tag, uid))
        except Exception as ex:
            self.logger.error(
                f"Failed to add tag to the parsing queue: {tag.id}"
                f"reason: {ex}")

        self.logger.info(f"Tag added to the parsing queue: {tag.id}")

    def get_progress(self, tag_id: int) -> Optional[Tuple[ParsingProgress, Tag]]:
        progress: Optional[Tuple[ParsingProgress, Tag]] = None

        try:
            with self.progress_lock:
                progress = copy.deepcopy(self.active_tags_storage[tag_id])
        except KeyError:
            pass

        return progress

    def del_progress(self, tag_id: int):
        with self.progress_lock:
            del self.active_tags_storage[tag_id]
