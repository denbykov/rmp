from abc import ABC, abstractmethod
from typing import *

from .Entities.DataError import *
from .Entities.UserCredentials import *
from source.Business.Entities.File.File import *


class IDataAccessor(ABC):
    @abstractmethod
    def get_password(self, login) -> Tuple[DataError, str]:
        pass

    @abstractmethod
    def add_user(self, credentials: UserCredentials) -> Tuple[DataError, str]:
        pass

    @abstractmethod
    def add_file(self, file: File, state_id: int) -> Tuple[DataError, File]:
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
