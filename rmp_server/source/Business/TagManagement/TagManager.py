from source.Business.IDataAccessor import *

from source.Business.Entities.Tag.Tag import *
from source.Business.Entities.File.FileSourceInfo import *
from source.Business.Entities.DataError import *

# from .DownloadingManager import *

import logging
import source.LoggerNames as LoggerNames

from pathlib import Path

from typing import *


class TagManager:
    db_tag_sources_id_mapping: Dict[TagSourceName, int]
    db_states_id_mapping: Dict[TagStateName, int]
    file_dir: Path = Path()
    parsing_manager: IDownloadingManager = DownloadingManager()
    apic_dir: Path = "apic"

    def __init__(self, data_accessor: IDataAccessor):
        self.data_accessor: IDataAccessor = data_accessor
        self.logger: logging.Logger = logging.getLogger(LoggerNames.BUSINESS)

    @classmethod
    def init(cls, data_accessor: IDataAccessor, file_dir: Path):
        logger: logging.Logger = logging.getLogger(LoggerNames.BUSINESS)
        logger.info(f"Initializing {cls.__name__} class")

        manager = cls(data_accessor)
        cls.db_tag_sources_id_mapping = manager._load_tag_sources_mapping()
        cls.db_states_id_mapping = manager._load_states_mapping()
        cls._init_dirs(file_dir)

        cls.parsing_manager.run()

        logger.info(f"Done initializing {cls.__name__} class")

    @classmethod
    def _init_dirs(cls, file_dir: Path):
        logger: logging.Logger = logging.getLogger(LoggerNames.BUSINESS)

        cls.file_dir = file_dir

        try:
            if not file_dir.is_dir():
                file_dir.mkdir()
            if not (file_dir / cls.apic_dir).is_dir():
                (file_dir / cls.apic_dir).mkdir()
        except Exception as ex:
            logger.error(f"Failed to create dirs, reason: {ex}")

    def _load_tag_sources_mapping(self) -> Dict[TagSourceName, int]:
        error, result = self.data_accessor.get_tag_sources()
        if error:
            raise RuntimeError("Failed to load tag sources")
        return result

    def _load_states_mapping(self) -> Dict[TagStateName, int]:
        error, result = self.data_accessor.get_tag_states()
        if error:
            raise RuntimeError("Failed to load tag states")
        return result

    def _restore_parsing_queue(self):
        self.logger.info("Restoring parsing")

        error, files = self.data_accessor.get_files_by_state(
            (TagStateName.PENDING,))
        if error:
            raise RuntimeError("Failed to fetch files to be restored")

        for file in files:
            self._enqueue_parsing(file)

        self.logger.info("parsing restored")

    def _enqueue_parsing(
            self,
            tag: Tag,
            file_source_info: Optional[FileSourceInfo] = None) \
            -> None:
        self.parsing_manager.enqueue_tag(tag, file_source_info)

    def parse_native_tag(self, tag: Tag, file_source_info: FileSourceInfo) \
            -> Tuple[DataError, Tag]:
        try:
            tag.apic = self._create_native_apic_file_path(tag, file_source_info)
            # Todo: check path correctness
        except RuntimeError:
            return DataError(True, ErrorCodes.BAD_ARGUMENT), tag

        tag.source = TagSource(
            self.db_tag_sources_id_mapping[TagSourceName.NATIVE],
            TagSourceName.NATIVE)

        tag.state = TagState(
            self.db_states_id_mapping[TagStateName.PENDING],
            TagStateName.PENDING
        )

        error, tag = self.data_accessor.add_tag(tag)

        if not error:
            self._enqueue_parsing(tag)

        return error, tag

    def _create_native_apic_file_path(
            self,
            tag: Tag,
            file_source_info: FileSourceInfo) -> Path:
        uid = str()

        for el in file_source_info.uid:
            if el.isupper():
                uid += el.lower() + el.lower()
            else:
                uid += el

        return \
            self.file_dir / \
            self.apic_dir / \
            f"{file_source_info.source.value}" \
            f"_{uid}" \
            f"_{tag.source.get_abbreviation()}."
