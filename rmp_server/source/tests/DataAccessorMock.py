from source.Business.IDataAccessor import *


class DataAccessorMock(IDataAccessor):
    def get_password(self, login) -> Tuple[DataError, str]:
        pass

    def add_user(self, credentials: UserCredentials) -> DataError:
        pass

    def add_file(self, file: File) -> Tuple[DataError, File]:
        pass

    def get_file(self, file_id: int) -> Tuple[DataError, File]:
        pass

    def update_file(self, file: File, state_id: int) -> Tuple[DataError, None]:
        pass

    def get_file_by_url(self, url: str) -> Tuple[DataError, File]:
        pass

    def get_file_states(self) -> Tuple[DataError, Dict[FileStateName, int]]:
        pass

    def get_files_by_state(self, states: Tuple[FileStateName, ...]) \
            -> Tuple[DataError, List[File]]:
        pass

    def update_file_state(self, file_id: int, state: FileState)\
            -> Tuple[DataError, None]:
        pass

    def get_tag_sources(self) -> Tuple[DataError, Dict[TagSourceName, int]]:
        pass

    def get_tag_states(self) -> Tuple[DataError, Dict[TagStateName, int]]:
        pass

    def add_tag(self, tag: Tag) \
            -> Tuple[DataError, Tag]:
        pass

    def get_tags_by_state(self, states: Tuple[TagStateName, ...]) \
            -> Tuple[DataError, List[Tag]]:
        pass

    def update_tag_state(self, tag_id: int, state: TagState) \
            -> Tuple[DataError, None]:
        pass

    def get_tag(self, tag_id: int) -> Tuple[DataError, Tag]:
        pass

    def update_tag(self, tag: Tag) \
            -> Tuple[DataError, None]:
        pass

    def get_native_tag_for_file(
            self,
            file_id: int,
            native_tag_sources: Tuple[int]) -> Tuple[DataError, Tag]:
        pass

    def get_tags(self, file_id: int) -> Tuple[DataError, List[Tag]]:
        pass

    def add_tag_mapping(self, mapping: TagMapping) \
            -> Tuple[DataError, TagMapping]:
        pass

    def update_tag_mapping(
            self,
            mapping: TagMapping) \
            -> Tuple[DataError, None]:
        pass

    def get_tag_mapping(
            self,
            mapping_id: int) \
            -> Tuple[DataError, TagMapping]:
        pass

    def get_tag_mapping_by_file(
            self,
            file_id: int) \
            -> Tuple[DataError, TagMapping]:
        pass
