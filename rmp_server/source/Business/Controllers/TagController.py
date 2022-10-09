import source.Business.TagManagement.TagManager as tm

from source.Business.IDataAccessor import *
from source.Business.IFileAccessor import IFileAccessor

from source.Business.Entities.APIError import *

from source.Business.URLParser import *


class TagController:
    def __init__(self, data_accessor: IDataAccessor, file_accessor: IFileAccessor):
        self.data_accessor: IDataAccessor = data_accessor
        self.file_accessor: IFileAccessor = file_accessor
        self.tag_manager = tm.TagManager(data_accessor)

    def pase_native_tag(self, file_id: int) -> Union[APIError, Tag]:
        tag = Tag(
            id=0,
            file_id=file_id,
            source=None,
            state=None,
            name='',
            artist='',
            lyrics='',
            year=0,
            apic_path=Path()
        )

        error, file = self.data_accessor.get_file(file_id)

        if error and error.code == ErrorCodes.NO_SUCH_RESOURCE:
            return APIError(error.code, "No such file")

        info: FileSourceInfo = URLParser.parse(file.url)

        error, tag = self.tag_manager.parse_native_tag(tag, info)

        if error:
            return self._get_error_response(error)

        return tag

    def pase_tags(
            self,
            file_id: int,
            tag_sources: List[TagSourceName]) -> Union[APIError, List[Tag]]:
        tags: List[Tag] = list()
        for el in tag_sources:
            tag = Tag(
                id=0,
                file_id=file_id,
                source=None,
                state=None,
                name='',
                artist='',
                lyrics='',
                year=0,
                apic_path=Path()
            )

            error, tag = self.tag_manager.parse_tag(tag, el)

            if error:
                return self._get_error_response(error)

            tags.append(tag)

        return tags

    def get_tag_state(self, tag_id: int) -> Union[APIError, TagState]:
        error, tag_state = self.tag_manager.get_state(tag_id)

        if error:
            return self._get_error_response(error)

        return tag_state

    @staticmethod
    def _get_error_response(error: DataError) -> APIError:
        if error.code == ErrorCodes.NO_SUCH_RESOURCE:
            return APIError(error.code, "No such tag")
        if error.code == ErrorCodes.UNKNOWN_ERROR:
            return APIError(error.code, "Unknown error")
        if error.code == ErrorCodes.BAD_ARGUMENT:
            return APIError(error.code, "Bad argument")
        if error.code == ErrorCodes.RESOURCE_ALREADY_EXISTS:
            return APIError(error.code, "Tag already exists")
        if error.code == ErrorCodes.PREREQUISITES_ARENT_MET:
            return APIError(error.code, "Prerequisites aren't met")

    @staticmethod
    def _get_tag_mapping_error_response(error: DataError) -> APIError:
        if error.code == ErrorCodes.NO_SUCH_RESOURCE:
            return APIError(error.code, "No such tag mapping")
        return TagController._get_error_response(error)

    def get_tags(self, file_id: int) -> Union[APIError, List[Tag]]:
        error, tags = self.data_accessor.get_tags(file_id)

        if error and error.code == ErrorCodes.NO_SUCH_RESOURCE:
            return APIError(error.code, "No such file")

        if error:
            return self._get_error_response(error)

        return tags

    def get_apic(self, url: str) -> Union[APIError, Tuple[bytes, str]]:
        path: Path = Path(url)
        filename: str = path.name
        extension: str = ""
        try:
            extension = path.name.split(".")[1]
        except IndexError:
            if not self.file_accessor.exists(path):
                return APIError(ErrorCodes.BAD_ARGUMENT, "Bad argument")

        path = self.tag_manager.file_dir / self.tag_manager.apic_dir / filename

        if not self.file_accessor.exists(path):
            return APIError(ErrorCodes.NO_SUCH_RESOURCE, "No such file")

        data = self.file_accessor.read_file(path)

        return data, extension

    def create_tag_mapping(self, file_id: int) -> Union[APIError, TagMapping]:
        error, mapping = self.tag_manager.create_tag_mapping(file_id)

        if error:
            return self._get_error_response(error)

        return mapping

    def get_tag_mapping(self, mapping_id: int) -> Union[APIError, TagMapping]:
        error, mapping = self.data_accessor.get_tag_mapping(mapping_id)

        if error:
            return self._get_tag_mapping_error_response(error)

        return mapping

    def get_tag_mapping_by_file(self, file_id: int) -> Union[APIError, TagMapping]:
        error, mapping = self.data_accessor.get_tag_mapping_by_file(file_id)

        if error:
            return self._get_tag_mapping_error_response(error)

        return mapping

    def update_tag_mapping(self, mapping: TagMapping) -> Union[APIError, None]:
        error, unused = self.data_accessor.update_tag_mapping(mapping)

        if error:
            return self._get_tag_mapping_error_response(error)

        return None

    def get_tag_sources(self) -> Union[APIError, List[TagSource]]:
        result: List[TagSource] = list()
        mapping: Dict[TagSourceName, int] = self.tag_manager.db_sources_id_mapping
        for el in mapping:
            result.append(TagSource(mapping[el], el))
        return result
