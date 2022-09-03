from abc import ABC, abstractmethod
from typing import *

from .Entities.DataError import *
from .Entities.UserCredentials import *
from source.Business.Entities.File.File import *

from source.Business.Entities.Tag.Tag import *


class IDataAccessor(ABC):
    @abstractmethod
    def get_password(self, login) -> Tuple[DataError, str]:
        pass

    @abstractmethod
    def add_user(self, credentials: UserCredentials) -> Tuple[DataError, str]:
        pass

    @abstractmethod
    def add_file(self, file: File) -> Tuple[DataError, File]:
        pass

    @abstractmethod
    def get_file(self, file_id: int) -> Tuple[DataError, File]:
        pass

    @abstractmethod
    def update_file_state(self, file_id: int, state: FileState)\
            -> Tuple[DataError, None]:
        pass

    @abstractmethod
    def get_file_by_url(self, url: str) -> Tuple[DataError, File]:
        pass

    @abstractmethod
    def get_file_states(self) -> Tuple[DataError, Dict[FileStateName, int]]:
        pass

    @abstractmethod
    def get_files_by_state(self, states: Tuple[FileStateName, ...])\
            -> Tuple[DataError, List[File]]:
        pass

    @abstractmethod
    def get_tag_sources(self) -> Tuple[DataError, Dict[TagSourceName, int]]:
        pass

    @abstractmethod
    def get_tag_states(self) -> Tuple[DataError, Dict[TagStateName, int]]:
        pass

    @abstractmethod
    def add_tag(self, tag: Tag) \
            -> Tuple[DataError, Tag]:
        pass

    @abstractmethod
    def get_tags_by_state(self, states: Tuple[TagStateName, ...]) \
            -> Tuple[DataError, List[Tag]]:
        pass

    @abstractmethod
    def update_tag_state(self, tag_id: int, state: TagState) \
            -> Tuple[DataError, None]:
        pass

    @abstractmethod
    def update_tag(self, tag: Tag) \
            -> Tuple[DataError, None]:
        pass

    @abstractmethod
    def get_tag(self, tag_id: int) -> Tuple[DataError, Tag]:
        pass

    @abstractmethod
    def get_native_tag_for_file(
            self,
            file_id: int,
            native_tag_sources: Tuple[int]) -> Tuple[DataError, Tag]:
        pass
