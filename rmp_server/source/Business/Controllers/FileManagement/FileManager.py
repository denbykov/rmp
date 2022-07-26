from source.Business.IDataAccessor import *
from source.Business.Parsers.URLParser import *

from .DownloadingManager import *

import logging
import source.LoggerNames as LoggerNames

from pathlib import Path


class FileManager:
    db_states_id_mapping: Dict[FileStateName, int]
    file_dir: Path = Path()
    downloading_manager: IDownloadingManager = DownloadingManager()
    audio_dir: Path = "audio"

    def __init__(self, data_accessor: IDataAccessor):
        self.data_accessor: IDataAccessor = data_accessor
        self.logger: logging.Logger = logging.getLogger(LoggerNames.BUSINESS)

    @classmethod
    def init(cls, data_accessor: IDataAccessor, file_dir: Path):
        logger: logging.Logger = logging.getLogger(LoggerNames.BUSINESS)
        logger.info("Initializing FileManager class")

        manager = cls(data_accessor)
        cls.db_states_id_mapping = manager._load_states_mapping()
        cls._init_dirs(file_dir)

        cls.downloading_manager.run()

        manager._restore_downloads()

        logger.info("Done initializing FileManager class")

    @classmethod
    def _init_dirs(cls, file_dir: Path):
        logger: logging.Logger = logging.getLogger(LoggerNames.BUSINESS)

        cls.file_dir = file_dir

        try:
            if not file_dir.is_dir():
                file_dir.mkdir()
            if not (file_dir / cls.audio_dir).is_dir():
                (file_dir / cls.audio_dir).mkdir()
        except Exception as ex:
            logger.error(f"Failed to create dirs, reason: {ex}")

    def _load_states_mapping(self) -> Dict[FileStateName, int]:
        error, result = self.data_accessor.get_file_states()
        if error:
            raise RuntimeError("Failed to load default file states")
        return result

    def _restore_downloads(self):
        self.logger.info("Restoring downloads")

        error, files = self.data_accessor.get_files_by_state(
            (FileStateName.PENDING,))
        if error:
            raise RuntimeError("Failed to fetch files to be restored")

        for file in files:
            self._enqueue_downloading(file)

        self.logger.info("Downloads restored")

    def _enqueue_downloading(self, file: File) -> None:
        self.downloading_manager.enqueue_file(file, URLParser.parse(file.url))

    def download_file(self, file: File) -> Tuple[DataError, File]:
        try:
            file.path = self._create_file_path(file)
            # Todo: check path correctness
        except RuntimeError:
            return DataError(True, ErrorCodes.BAD_ARGUMENT), file

        file.state = FileState(
            self.db_states_id_mapping[FileStateName.PENDING],
            FileStateName.PENDING,
            "")

        error, file = self.data_accessor.add_file(
            file, self.db_states_id_mapping[FileStateName.PENDING])

        if not error:
            self._enqueue_downloading(file)

        return error, file

    def get_state(self, file_id: int) -> Tuple[DataError, FileState]:
        progress: Optional[DownloadingProgress] =\
            self.downloading_manager.get_progress(file_id)

        if progress:
            return self.get_state_from_progress(progress, file_id)

        error, file = self.data_accessor.get_file(file_id)

        return error, file.state

    def get_state_from_progress(self, progress: DownloadingProgress, file_id: int)\
            -> Tuple[DataError, FileState]:
        error = DataError(False, ErrorCodes.UNKNOWN_ERROR)
        state: FileState = FileState(0, progress.state, "")

        if progress.state == FileStateName.LOADING:
            state.description = f"{progress.percent}|{progress.speed}"
            return error, state
        if progress.state == FileStateName.CONVERTING:
            return error, state
        if progress.state == FileStateName.READY:
            state.id = self.db_states_id_mapping[FileStateName.READY]
            error, ignored = self.data_accessor.update_file_state(file_id, state)
            self.downloading_manager.del_progress(file_id)

            return error, state

    def _create_file_path(self, file: File) -> Path:
        info = URLParser.parse(file.url)

        uid = str()

        for el in info.uid:
            if el.isupper():
                uid += el.lower() + el.lower()
            else:
                uid += el

        return \
            FileManager.file_dir / \
            FileManager.audio_dir / \
            f"{info.source.value}_{uid}.mp3"
