import typing

import source.Business.Controllers.FileManagement.FileManager as fm

from source.Business.IDataAccessor import *

from source.Business.Entities.APIError import *


class FileController:
    def __init__(self, data_accessor: IDataAccessor):
        self.data_accessor: IDataAccessor = data_accessor
        self.file_manager = fm.FileManager(data_accessor)

    def download_file(self, url: str) -> Union[APIError, File]:
        file = File(url=url, id=None, path=None, state=None)

        error, file = self.file_manager.download_file(file)

        if error and error.code == ErrorCodes.RESOURCE_ALREADY_EXISTS:
            return APIError(error.code, "File already exists")
        if error and error.code == ErrorCodes.UNKNOWN_ERROR:
            return APIError(error.code, "Unknown error")
        if error and error.code == ErrorCodes.BAD_ARGUMENT:
            return APIError(error.code, "Bad argument")

        return file

    def get_file_state(self, file_id: int) -> Union[APIError, FileState]:
        error, file_state = self.file_manager.get_state(file_id)

        if error and error.code == ErrorCodes.NO_SUCH_RESOURCE:
            return APIError(error.code, "No such file")
        if error and error.code == ErrorCodes.UNKNOWN_ERROR:
            return APIError(error.code, "Unknown error")
        if error and error.code == ErrorCodes.BAD_ARGUMENT:
            return APIError(error.code, "Bad argument")

        return file_state

    def get_file(self, file_id: int) -> Union[APIError, bytes]:
        error, data = self.file_manager.get_file(file_id)

        if error and error.code == ErrorCodes.NO_SUCH_RESOURCE:
            return APIError(error.code, "No such file")
        if error and error.code == ErrorCodes.UNKNOWN_ERROR:
            return APIError(error.code, "Unknown error")
        if error and error.code == ErrorCodes.BAD_ARGUMENT:
            return APIError(error.code, "Bad argument")

        return data

    def find_file(self, url: str) -> Union[APIError, File]:
        error, file = self.data_accessor.get_file_by_url(url)

        if error and error.code == ErrorCodes.NO_SUCH_RESOURCE:
            return APIError(error.code, "No such file")
        if error and error.code == ErrorCodes.UNKNOWN_ERROR:
            return APIError(error.code, "Unknown error")
        if error and error.code == ErrorCodes.BAD_ARGUMENT:
            return APIError(error.code, "Bad argument")

        return file
