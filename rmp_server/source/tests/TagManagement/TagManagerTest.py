import unittest
from unittest.mock import *

from source.tests.DataAccessorMock import *
from .ParsingManagerMock import *

from source.Data.utils import *

from source.Business.TagManagement.TagManager import TagManager
from source.Presentation.Parsers.URLParser import *

tag_states = {
    TagStateName.ERROR: 1,
    TagStateName.PENDING: 2,
    TagStateName.READY: 3}

tag_state_pending: TagState = TagState(
    tag_states[TagStateName.PENDING],
    TagStateName.PENDING
)

tag_state_ready: TagState = TagState(
    tag_states[TagStateName.READY],
    TagStateName.READY
)

tag_state_parsing: TagState = TagState(
    0,
    TagStateName.PARSING
)

tag_progress_parsing: ParsingProgress = ParsingProgress(
    TagStateName.PARSING)

tag_progress_ready: ParsingProgress = ParsingProgress(
    TagStateName.READY)

tag_sources = {
    TagSourceName.NATIVE_YT: 1,
    TagSourceName.SPOTIFY: 2,
    TagSourceName.ITUNES: 3,
    TagSourceName.CELERIS_GOOGLE_SEARCH: 4
}

tag_sources_nt_yt: TagSource = TagSource(
    tag_sources[TagSourceName.NATIVE_YT],
    TagSourceName.NATIVE_YT
)

pending_tag_1 = Tag(
    id=1,
    file_id=1,
    source=tag_sources_nt_yt,
    state=tag_state_pending,
    name="",
    artist="",
    lyrics="",
    year=0,
    apic_path=Path("storage\\apic\\yt_4a8ccogwwaa3-yy.nt-yt")
)

raw_tag_1 = Tag(
    id=0,
    file_id=1,
    source=None,
    state=None,
    name="",
    artist="",
    lyrics="",
    year=0,
    apic_path=Path()
)

prefilled_tag_1 = Tag(
    id=0,
    file_id=1,
    source=tag_sources_nt_yt,
    state=tag_state_pending,
    name="",
    artist="",
    lyrics="",
    year=0,
    apic_path=Path("storage\\apic\\yt_4a8ccogwwaa3-yy.nt-yt")
)

ready_tag_1 = Tag(
    id=1,
    file_id=1,
    source=tag_sources_nt_yt,
    state=tag_state_ready,
    name="",
    artist="",
    lyrics="",
    year=0,
    apic_path=Path("storage\\apic\\yt_4a8ccogwwaa3-yy.nt-yt")
)


file_states = {
    FileStateName.ERROR: 1,
    FileStateName.PENDING: 2,
    FileStateName.READY: 3}

file_state_pending: FileState = FileState(
    file_states[FileStateName.PENDING],
    FileStateName.PENDING,
    ""
)

pending_file_1 = File(
    id=1,
    url="https://www.youtube.com/watch?v=4a8CogWA3-Y&",
    path=Path("storage\\audio\\yt_4a8ccogwwaa3-yy.mp3"),
    state=file_state_pending)


class TagManagerTest(unittest.TestCase):
    def setUp(self):
        self.data_accessor = DataAccessorMock()
        self.tag_manager = TagManager(self.data_accessor)
        self.parsing_manager = ParsingManagerMock()
        TagManager.parsing_manager = self.parsing_manager
        TagManager.db_states_id_mapping = tag_states
        TagManager.db_sources_id_mapping = tag_sources
        TagManager.file_dir = Path("storage")

    def test_init(self):
        self.data_accessor.get_tag_states = \
            create_autospec(
                self.data_accessor.get_tag_states,
                return_value=make_da_response(
                    result=tag_states))

        self.data_accessor.get_tag_sources = \
            create_autospec(
                self.data_accessor.get_tag_sources,
                return_value=make_da_response(
                    result=tag_sources))

        self.data_accessor.get_tags_by_state = \
            create_autospec(
                self.data_accessor.get_tags_by_state,
                return_value=make_da_response(result=(
                    pending_tag_1,)))

        self.data_accessor.get_file = \
            create_autospec(
                self.data_accessor.get_file,
                return_value=make_da_response(result=pending_file_1))

        self.parsing_manager.run = \
            create_autospec(
                self.parsing_manager.run,
                return_value=None)

        self.parsing_manager.enqueue_native_tag = \
            create_autospec(
                self.parsing_manager.enqueue_native_tag,
                return_value=None)

        TagManager.db_states_id_mapping = None
        TagManager.file_dir = None

        file_dir: Path = Path("storage")

        self.tag_manager.init(
            self.parsing_manager,
            self.data_accessor,
            file_dir)

        self.data_accessor.get_tag_states.assert_called_once()
        self.data_accessor.get_tag_sources.assert_called_once()
        self.data_accessor.get_tags_by_state.assert_called_once_with(
            (TagStateName.PENDING,))
        self.data_accessor.get_file.assert_called_once_with(
            pending_tag_1.file_id)

        TagManager.parsing_manager.run.assert_called_once()
        TagManager.parsing_manager.enqueue_native_tag.assert_has_calls(
            (
                call(pending_tag_1, URLParser.parse(pending_file_1.url).uid),
            ))

        self.assertEqual(self.tag_manager.db_states_id_mapping, tag_states)
        self.assertEqual(self.tag_manager.db_sources_id_mapping, tag_sources)
        self.assertEqual(self.tag_manager.file_dir, file_dir)

    def test_(self):
        self.data_accessor.add_tag = \
            create_autospec(
                self.data_accessor.add_tag,
                return_value=make_da_response(
                    result=pending_tag_1))

        TagManager.parsing_manager.enqueue_native_tag = \
            create_autospec(
                TagManager.parsing_manager.enqueue_native_tag,
                return_value=None)

        error, tag = self.tag_manager.parse_native_tag(
            raw_tag_1,
            URLParser.parse(pending_file_1.url))

        self.data_accessor.add_tag.assert_called_once_with(prefilled_tag_1)
        TagManager.parsing_manager.enqueue_native_tag.assert_called_once_with(
            pending_tag_1, URLParser.parse(pending_file_1.url).uid)

        self.assertEqual(tag, pending_tag_1)
        self.assertEqual(bool(error), False)

    def test_get_state_pending(self):
        TagManager.parsing_manager.get_progress = \
            create_autospec(
                TagManager.parsing_manager.get_progress,
                return_value=None)

        self.data_accessor.get_tag = \
            create_autospec(
                self.data_accessor.get_tag,
                return_value=make_da_response(
                    result=pending_tag_1))

        error, tag_state = self.tag_manager.get_state(1)

        TagManager.parsing_manager.get_progress.assert_called_once_with(1)
        self.data_accessor.get_tag.assert_called_once_with(1)

        self.assertEqual(tag_state, tag_state_pending)
        self.assertEqual(bool(error), False)

    def test_get_state_parsing(self):
        TagManager.parsing_manager.get_progress = \
            create_autospec(
                TagManager.parsing_manager.get_progress,
                return_value=[tag_progress_parsing, pending_tag_1])

        self.data_accessor.get_tag = \
            create_autospec(
                self.data_accessor.get_tag,
                return_value=make_da_response(
                    result=pending_tag_1))

        error, tag_state = self.tag_manager.get_state(1)

        TagManager.parsing_manager.get_progress.assert_called_once_with(1)
        self.data_accessor.get_tag.assert_not_called()

        self.assertEqual(tag_state, tag_state_parsing)
        self.assertEqual(bool(error), False)

    def test_get_state_ready(self):
        TagManager.parsing_manager.get_progress = \
            create_autospec(
                TagManager.parsing_manager.get_progress,
                return_value=[tag_progress_ready, ready_tag_1])

        self.data_accessor.get_tag = \
            create_autospec(
                self.data_accessor.get_tag,
                return_value=make_da_response(
                    result=pending_tag_1))

        self.data_accessor.update_tag = \
            create_autospec(
                self.data_accessor.update_tag,
                return_value=make_da_response(
                    result=None))

        TagManager.parsing_manager.del_progress = \
            create_autospec(
                TagManager.parsing_manager.del_progress,
                return_value=None)

        error, tag_state = self.tag_manager.get_state(1)

        TagManager.parsing_manager.get_progress.assert_called_once_with(1)
        self.data_accessor.update_tag.assert_called_once_with(
            ready_tag_1)
        TagManager.parsing_manager.del_progress.assert_called_once_with(1)
        self.data_accessor.get_tag.assert_not_called()

        self.assertEqual(tag_state, tag_state_ready)
        self.assertEqual(bool(error), False)
