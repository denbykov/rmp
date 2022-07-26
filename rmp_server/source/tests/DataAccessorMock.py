from source.Business.IDataAccessor import *


class DataAccessorMock(IDataAccessor):
    def get_password(self, login) -> Tuple[DataError, str]:
        pass

    def add_user(self, credentials: UserCredentials) -> DataError:
        pass

    def add_file(self, file: File, state_id: int) -> Tuple[DataError, File]:
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
