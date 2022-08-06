from source.Business.IDataAccessor import *
from .UserRepository import *
from .FileRepository import *
from .TagRepository import *


class DataAccessor(IDataAccessor):
    def __init__(self, con):
        self.con = con
        self.user_repository = UserRepository()
        self.file_repository = FileRepository()
        self.tag_repository = TagRepository()

    # user repo
    def get_password(self, login) -> Tuple[DataError, str]:
        return self.user_repository.get_password(login, self.con)

    def add_user(self, credentials: UserCredentials) -> Tuple[DataError, None]:
        return self.user_repository.add_user(credentials, self.con)

    # file repo
    def add_file(self, file: File) -> Tuple[DataError, File]:
        return self.file_repository.add_file(file, self.con)

    def get_file(self, file_id: int) -> Tuple[DataError, File]:
        return self.file_repository.get_file(file_id, self.con)

    def update_file_state(self, file_id: int, state: FileState) -> Tuple[DataError, None]:
        return self.file_repository.update_file_state(file_id, state, self.con)

    def get_file_by_url(self, url: str) -> Tuple[DataError, File]:
        return self.file_repository.get_file_by_url(url, self.con)

    def get_file_states(self) -> Tuple[DataError, Dict[FileStateName, int]]:
        return self.file_repository.get_file_states(self.con)

    def get_files_by_state(self, states: Tuple[FileStateName, ...])\
            -> Tuple[DataError, List[File]]:
        return self.file_repository.get_files_by_state(states, self.con)

    # tag repo
    def get_tag_sources(self) -> Tuple[DataError, Dict[TagSource, int]]:
        return self.tag_repository.get_tag_sources(self.con)

    def get_tag_states(self) -> Tuple[DataError, Dict[TagStateName, int]]:
        return self.tag_repository.get_tag_states(self.con)
