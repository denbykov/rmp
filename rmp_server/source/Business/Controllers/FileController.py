import source.Business.FileManagement.FileManager as fm
import source.Business.TagManagement.TagManager as tm

from source.Business.IDataAccessor import *

from source.Business.Entities.APIError import *
from source.Business.IFileAccessor import IFileAccessor


class FileController:
    def __init__(self, data_accessor: IDataAccessor, file_accessor: IFileAccessor):
        self.data_accessor: IDataAccessor = data_accessor
        self.file_accessor: IFileAccessor = file_accessor
        self.file_manager = fm.FileManager(data_accessor, file_accessor)
        self.tag_manager = tm.TagManager(data_accessor)

    def download_file(self, url: str) -> Union[APIError, File]:
        file = File(url=url, id=None, path=None, state=None)

        error, file = self.file_manager.download_file(file)

        if error:
            return self._get_error_response(error)

        return file

    def get_file_state(self, file_id: int) -> Union[APIError, FileState]:
        error, file_state = self.file_manager.get_state(file_id)

        if error:
            return self._get_error_response(error)

        return file_state

    def get_file(self, file_id: int, apply_tags: bool = False) \
            -> Union[APIError, bytes]:
        error, data = self.file_manager.get_file(file_id)

        if error:
            return self._get_error_response(error)

        if apply_tags:
            tag: Optional[Tag]
            error, tag = self.tag_manager.form_tag_for_file(file_id)

            if error:
                return self._get_tag_error_response(error)

            image: bytes = self.file_accessor.read_file(tag.apic_path)

            data = self.file_accessor.apply_tag(data, tag, image)

        return data

    def find_file(self, url: str) -> Union[APIError, File]:
        error, file = self.data_accessor.get_file_by_url(url)

        if error:
            return self._get_error_response(error)

        return file

    @staticmethod
    def _get_error_response(error: DataError) -> APIError:
        if error.code == ErrorCodes.NO_SUCH_RESOURCE:
            return APIError(error.code, "No such file")
        if error.code == ErrorCodes.UNKNOWN_ERROR:
            return APIError(error.code, "Unknown error")
        if error.code == ErrorCodes.BAD_ARGUMENT:
            return APIError(error.code, "Bad argument")
        if error.code == ErrorCodes.RESOURCE_ALREADY_EXISTS:
            return APIError(error.code, "File already exists")

    @staticmethod
    def _get_tag_error_response(error: DataError) -> APIError:
        if error.code == ErrorCodes.NO_SUCH_RESOURCE:
            return APIError(error.code, "Unable to obtain some tag")
        return FileController._get_error_response(error)
