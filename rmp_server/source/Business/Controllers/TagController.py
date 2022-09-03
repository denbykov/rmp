import source.Business.TagManagement.TagManager as tm

from source.Business.IDataAccessor import *

from source.Business.Entities.APIError import *

from source.Presentation.Parsers.URLParser import *


class TagController:
    def __init__(self, data_accessor: IDataAccessor):
        self.data_accessor: IDataAccessor = data_accessor
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
