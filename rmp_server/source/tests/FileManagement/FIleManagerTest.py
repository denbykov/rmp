import unittest
from unittest.mock import *

from source.tests.DataAccessorMock import *
from .DownloadingManagerMock import *

from source.Data.utils import *

from source.Business.FileManagement.FileManager import FileManager
from source.Presentation.Parsers.URLParser import *

file_states = {
    FileStateName.ERROR: 1,
    FileStateName.PENDING: 2,
    FileStateName.READY: 3}

file_state_pending: FileState = FileState(
    file_states[FileStateName.PENDING],
    FileStateName.PENDING,
    ""
)

file_progress_loading: DownloadingProgress = DownloadingProgress(
    1, 1, FileStateName.LOADING)

file_state_loading: FileState = FileState(
    0,
    FileStateName.LOADING,
    "1|1"
)

file_progress_converting: DownloadingProgress = DownloadingProgress(
    0, 0, FileStateName.CONVERTING)

file_state_converting: FileState = FileState(
    0,
    FileStateName.CONVERTING,
    ""
)

file_progress_ready: DownloadingProgress = DownloadingProgress(
    0, 0, FileStateName.READY)

file_state_ready: FileState = FileState(
    file_states[FileStateName.READY],
    FileStateName.READY,
    ""
)

raw_file_1 = File(
    id=None,
    url="https://www.youtube.com/watch?v=4a8CogWA3-Y&",
    path=None,
    state=None)

prefilled_file_1 = File(
    id=None,
    url="https://www.youtube.com/watch?v=4a8CogWA3-Y&",
    path=Path("storage\\audio\\yt_4a8ccogwwaa3-yy.mp3"),
    state=file_state_pending)

pending_file_1 = File(
    id=1,
    url="https://www.youtube.com/watch?v=4a8CogWA3-Y&",
    path=Path("storage\\audio\\yt_4a8ccogwwaa3-yy.mp3"),
    state=file_state_pending)

pending_file_2 = File(
    id=2,
    url="https://www.youtube.com/watch?v=4a8CogWA3-C&",
    path=Path("storage\\audio\\yt_4a8ccogwwaa3-cc.mp3"),
    state=file_state_pending)


class FileManagerTest(unittest.TestCase):
    def setUp(self):
        self.data_accessor = DataAccessorMock()
        self.file_manager = FileManager(self.data_accessor)
        FileManager.downloading_manager = DownloadingManagerMock()
        FileManager.db_states_id_mapping = file_states
        FileManager.file_dir = Path("storage")

    def test_init(self):
        self.data_accessor.get_file_states = \
            create_autospec(
                self.data_accessor.get_file_states,
                return_value=make_da_response(
                    result=file_states))

        self.data_accessor.get_files_by_state = \
            create_autospec(
                self.data_accessor.get_files_by_state,
                return_value=make_da_response(result=[
                    pending_file_1,
                    pending_file_2]))

        FileManager.downloading_manager.run = \
            create_autospec(
                FileManager.downloading_manager.run,
                return_value=None)

        FileManager.downloading_manager.enqueue_file = \
            create_autospec(
                FileManager.downloading_manager.enqueue_file,
                return_value=None)

        FileManager.db_states_id_mapping = None
        FileManager.file_dir = None

        file_dir: Path = Path("storage")

        self.file_manager.init(self.data_accessor, file_dir)

        self.data_accessor.get_file_states.assert_called_once()
        self.data_accessor.get_files_by_state.assert_called_once_with(
            (FileStateName.PENDING,))
        FileManager.downloading_manager.run.assert_called_once()
        FileManager.downloading_manager.enqueue_file.assert_has_calls(
            [
                call(pending_file_1, URLParser.parse(pending_file_1.url)),
                call(pending_file_2, URLParser.parse(pending_file_2.url))
            ])

        self.assertEqual(self.file_manager.db_states_id_mapping, file_states)
        self.assertEqual(self.file_manager.file_dir, file_dir)

    def test_download_file(self):
        self.data_accessor.add_file = \
            create_autospec(
                self.data_accessor.add_file,
                return_value=make_da_response(
                    result=pending_file_1))

        FileManager.downloading_manager.enqueue_file = \
            create_autospec(
                FileManager.downloading_manager.enqueue_file,
                return_value=None)

        error, file = self.file_manager.download_file(raw_file_1)

        self.data_accessor.add_file.assert_called_once_with(prefilled_file_1)
        FileManager.downloading_manager.enqueue_file.assert_called_once_with(
            pending_file_1, URLParser.parse(pending_file_1.url))

        self.assertEqual(file, pending_file_1)
        self.assertEqual(bool(error), False)

    def test_get_state_pending(self):
        FileManager.downloading_manager.get_progress = \
            create_autospec(
                FileManager.downloading_manager.get_progress,
                return_value=None)

        self.data_accessor.get_file = \
            create_autospec(
                self.data_accessor.get_file,
                return_value=make_da_response(
                    result=pending_file_1))

        error, file_state = self.file_manager.get_state(1)

        FileManager.downloading_manager.get_progress.assert_called_once_with(1)
        self.data_accessor.get_file.assert_called_once_with(1)

        self.assertEqual(file_state, file_state_pending)
        self.assertEqual(bool(error), False)

    def test_get_state_loading(self):
        FileManager.downloading_manager.get_progress = \
            create_autospec(
                FileManager.downloading_manager.get_progress,
                return_value=file_progress_loading)

        self.data_accessor.get_file = \
            create_autospec(
                self.data_accessor.get_file,
                return_value=make_da_response(
                    result=pending_file_1))

        error, file_state = self.file_manager.get_state(1)

        FileManager.downloading_manager.get_progress.assert_called_once_with(1)
        self.data_accessor.get_file.assert_not_called()

        self.assertEqual(file_state, file_state_loading)
        self.assertEqual(bool(error), False)

    def test_get_state_converting(self):
        FileManager.downloading_manager.get_progress = \
            create_autospec(
                FileManager.downloading_manager.get_progress,
                return_value=file_progress_converting)

        self.data_accessor.get_file = \
            create_autospec(
                self.data_accessor.get_file,
                return_value=make_da_response(
                    result=pending_file_1))

        error, file_state = self.file_manager.get_state(1)

        FileManager.downloading_manager.get_progress.assert_called_once_with(1)
        self.data_accessor.get_file.assert_not_called()

        self.assertEqual(file_state, file_state_converting)
        self.assertEqual(bool(error), False)

    def test_get_state_ready(self):
        FileManager.downloading_manager.get_progress = \
            create_autospec(
                FileManager.downloading_manager.get_progress,
                return_value=file_progress_ready)

        self.data_accessor.get_file = \
            create_autospec(
                self.data_accessor.get_file,
                return_value=make_da_response(
                    result=pending_file_1))

        self.data_accessor.update_file_state = \
            create_autospec(
                self.data_accessor.update_file_state,
                return_value=make_da_response(
                    result=None))

        FileManager.downloading_manager.del_progress = \
            create_autospec(
                FileManager.downloading_manager.del_progress,
                return_value=None)

        error, file_state = self.file_manager.get_state(1)

        FileManager.downloading_manager.get_progress.assert_called_once_with(1)
        self.data_accessor.update_file_state.assert_called_once_with(
            1, file_state_ready)
        FileManager.downloading_manager.del_progress.assert_called_once_with(1)
        self.data_accessor.get_file.assert_not_called()

        self.assertEqual(file_state, file_state_ready)
        self.assertEqual(bool(error), False)
