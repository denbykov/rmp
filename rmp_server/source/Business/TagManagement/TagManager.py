from source.Business.IDataAccessor import *

from source.Business.Entities.DataError import *

from .IParsingManager import *

from source.Business.URLParser import *

import logging
import source.LoggerNames as LoggerNames

from pathlib import Path

from typing import *

from source.Business.IFileAccessor import IFileAccessor
from ..Entities.Tag.TagMapping import TagMapping


class TagManager:
    db_sources_id_mapping: Dict[TagSourceName, int]
    db_states_id_mapping: Dict[TagStateName, int]
    file_dir: Path = Path()
    parsing_manager: IParsingManager = None
    apic_dir: Path = "apic"

    def __init__(self, data_accessor: IDataAccessor):
        self.data_accessor: IDataAccessor = data_accessor
        self.logger: logging.Logger = logging.getLogger(LoggerNames.BUSINESS)

    @classmethod
    def init(
            cls,
            parsing_manager: IParsingManager,
            data_accessor: IDataAccessor,
            file_accessor: IFileAccessor,
            file_dir: Path):
        cls.parsing_manager = parsing_manager

        logger: logging.Logger = logging.getLogger(LoggerNames.BUSINESS)
        logger.info(f"Initializing {cls.__name__} class")

        manager = cls(data_accessor)
        cls.db_sources_id_mapping = manager._load_tag_sources_mapping()
        cls.db_states_id_mapping = manager._load_states_mapping()
        cls._init_dirs(file_dir, file_accessor)

        cls.parsing_manager.run()

        manager._restore_parsing_queue()

        logger.info(f"Done initializing {cls.__name__} class")

    @classmethod
    def _init_dirs(cls, file_dir: Path, file_accessor: IFileAccessor):
        logger: logging.Logger = logging.getLogger(LoggerNames.BUSINESS)

        cls.file_dir = file_dir

        try:
            file_accessor.make_dir(file_dir)
            file_accessor.make_dir(file_dir / cls.apic_dir)
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

        error, tags = self.data_accessor.get_tags_by_state(
            (TagStateName.PENDING,))
        if error:
            raise RuntimeError("Failed to fetch tags to be restored")

        for tag in tags:
            if tag.source.name in (TagSourceName.NATIVE_YT,):
                self._restore_native_tag_parsing(tag)
            else:
                pass

        self.logger.info(f"{len(tags)} tags restored for parsing")

    def _restore_native_tag_parsing(self, tag: Tag):
        error, file = self.data_accessor.get_file(tag.file_id)
        if error:
            raise RuntimeError(f"Failed to read file with id: {tag.file_id}")

        uid: str = URLParser.parse(file.url).uid

        self._enqueue_native_tag_parsing(tag, uid)

    def _enqueue_parsing(self, tag: Tag, native_tag: Tag) -> None:
        self.parsing_manager.enqueue_tag(tag, native_tag)

    def _enqueue_native_tag_parsing(self, tag: Tag, uid: str) -> None:
        self.parsing_manager.enqueue_native_tag(tag, uid)

    def parse_native_tag(
            self, tag: Tag, file_source_info: FileSourceInfo) \
            -> Tuple[DataError, Tag]:
        tag_source: TagSourceName = self._get_file_source(file_source_info)

        tag.source = TagSource(
            self.db_sources_id_mapping[tag_source], tag_source)

        tag.state = TagState(
            self.db_states_id_mapping[TagStateName.PENDING],
            TagStateName.PENDING)

        try:
            tag.apic_path = self._create_native_apic_file_path(tag, file_source_info)
        except RuntimeError:
            return DataError(True, ErrorCodes.BAD_ARGUMENT), tag

        error, tag = self.data_accessor.add_tag(tag)

        if not error:
            self._enqueue_native_tag_parsing(tag, file_source_info.uid)

        return error, tag

    def parse_tag(
            self, tag: Tag, tag_source: TagSourceName) \
            -> Tuple[DataError, Tag]:

        error, native_tag = self.data_accessor.get_native_tag_for_file(
            tag.file_id,
            self._form_native_tag_source_ids())

        if error:
            return error, tag

        if native_tag.state.name != TagStateName.READY:
            return DataError(True, ErrorCodes.PREREQUISITES_ARENT_MET), tag

        tag.source = TagSource(
            self.db_sources_id_mapping[tag_source], tag_source)

        tag.state = TagState(
            self.db_states_id_mapping[TagStateName.PENDING],
            TagStateName.PENDING)

        try:
            tag.apic_path = self._create_apic_file_path_from_native(
                tag, native_tag.source, native_tag.apic_path)
        except RuntimeError:
            return DataError(True, ErrorCodes.BAD_ARGUMENT), tag

        error, tag = self.data_accessor.add_tag(tag)

        if not error:
            self._enqueue_parsing(tag, native_tag)

        return error, tag

    def _form_native_tag_source_ids(self) -> Tuple[int]:
        return (
            self.db_sources_id_mapping[TagSourceName.NATIVE_YT],)

    @staticmethod
    def _get_file_source(info: FileSourceInfo) -> TagSourceName:
        if info.source == FileSource.YOUTUBE:
            return TagSourceName.NATIVE_YT

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
            f"_{uid}." \
            f"{tag.source.name.get_abbreviation()}"

    @staticmethod
    def _create_apic_file_path_from_native(
            tag: Tag,
            native_tag_source: TagSource,
            native_apic_path: Path) -> Path:
        suffix: str = str("".join(native_apic_path.suffixes))
        suffix = suffix.replace(
            native_tag_source.name.get_abbreviation(),
            tag.source.name.get_abbreviation())
        path: Path = Path()
        for el in native_apic_path.parts[0:-1]:
            path /= el
        path /= Path(native_apic_path.stem).stem
        path = path.with_suffix(suffix)
        return path

    def get_state(self, tag_id: int) -> Tuple[DataError, Optional[TagState]]:
        progress: Optional[Tuple[ParsingProgress, Tag]] =\
            self.parsing_manager.get_progress(tag_id)

        if progress:
            return self.get_state_from_progress(progress)

        error, tag = self.data_accessor.get_tag(tag_id)
        if error:
            return error, None
        return error, tag.state

    def get_state_from_progress(
            self, progress_data: Tuple[ParsingProgress, Tag])\
            -> Tuple[DataError, TagState]:
        error = DataError(False, ErrorCodes.UNKNOWN_ERROR)

        progress: ParsingProgress = progress_data[0]
        tag: Tag = progress_data[1]

        state: TagState = TagState(0, progress.state)

        if progress.state in self.db_states_id_mapping:
            state.id = self.db_states_id_mapping[progress.state]

        if progress.state == TagStateName.PARSING:
            return error, state
        if progress.state == TagStateName.ERROR:
            error, ignored = self.data_accessor.update_tag_state(tag.id, state)
            self.parsing_manager.del_progress(tag.id)
            return error, state
        if progress.state == TagStateName.READY:
            state.id = self.db_states_id_mapping[TagStateName.READY]
            tag.state = state
            error, ignored = self.data_accessor.update_tag(tag)
            self.parsing_manager.del_progress(tag.id)

            return error, state

    def create_tag_mapping(self, file_id: int) \
            -> Tuple[DataError, Optional[TagMapping]]:
        error, tag = self.data_accessor.get_native_tag_for_file(
            file_id,
            self._form_native_tag_source_ids())
        if error:
            return error, None

        mapping: TagMapping = TagMapping(
            id=0,
            file_id=file_id,
            name=tag.source,
            artist=tag.source,
            lyrics=tag.source,
            year=tag.source,
            apic=tag.source)

        error, mapping = self.data_accessor.add_tag_mapping(mapping)
        if error:
            return error, None

        return error, mapping

    def form_tag_for_file(self, file_id: int) \
            -> Tuple[DataError, Optional[Tag]]:
        error, mapping = self.data_accessor.get_tag_mapping_by_file(file_id)

        if error:
            return error, None

        error, tags = self.data_accessor.get_tags(file_id)

        if error:
            return error, None

        tag: Optional[Tag] = None

        try:
            tag = self._apply_tag_mapping(tags, mapping)
        except KeyError as ex:
            return DataError(True, ErrorCodes.NO_SUCH_RESOURCE), None

        return error, tag

    def _apply_tag_mapping(self, tags: List[Tag], mapping: TagMapping) \
            -> Tag:
        tag: Tag = Tag(None, None, None, None, None, None, None, None, None)

        tags_dict: Dict[int, Tag] = dict()
        for el in tags:
            tags_dict[el.source.id] = el

        tag.name = tags_dict[mapping.name.id].name
        tag.artist = tags_dict[mapping.artist.id].artist
        tag.lyrics = tags_dict[mapping.lyrics.id].lyrics
        tag.year = tags_dict[mapping.year.id].year
        tag.apic_path = tags_dict[mapping.apic.id].apic_path

        return tag
