from .AuthorizedHandler import *

# from source.Presentation.Parsers.FileURLParser import *
from source.Presentation.Formatters.Tag.TagFormatter import *
from source.Business.Controllers.TagController import *
from source.Presentation.Parsers.FileURLParser import FileURLParser
from source.Presentation.Formatters.Tag.TagMappingFormatter import *


class TagManagementHandler(AuthorizedHandler):
    def __init__(self, data_accessor: IDataAccessor, file_accessor: IFileAccessor, secret: str):
        super(TagManagementHandler, self).__init__(data_accessor, secret)
        self.controller: TagController = TagController(data_accessor, file_accessor)

    def authorized_handle(self, request: AuthorizedHTTPRequest) -> HTTPResponse:
        splitted_path = request.path.split('/')

        path = ""
        try:
            path = splitted_path[2]
        except IndexError:
            pass

        if path == "parse-native-tag" and request.method == HTTPMethod.POST:
            file_id = int(splitted_path[3])
            return self._parse_native_tag(file_id)

        if path == "find-by-file" and request.method == HTTPMethod.GET:
            file_id = int(splitted_path[3])
            return self._get_tags(file_id)

        if path == "find-apic" and request.method == HTTPMethod.POST:
            return self._get_apic(request)

        if path == "tags":
            tag_id = int(splitted_path[3])
            path = splitted_path[4]

            if path == "state" and request.method == HTTPMethod.GET:
                return self._get_tag_state(tag_id)

        if path == "tag-mappings":
            path = splitted_path[3]

            if path == "find-by-file" and request.method == HTTPMethod.GET:
                file_id = int(splitted_path[3])
                return self._get_tag_mapping_by_file(file_id)

            if request.method == HTTPMethod.GET:
                mapping_id = int(splitted_path[3])
                return self._get_tag_mapping(mapping_id)

            if request.method == HTTPMethod.POST:
                file_id = int(splitted_path[3])
                return self._create_tag_mapping(file_id)

            if request.method == HTTPMethod.POST:
                return self._update_tag_mapping(request)

        return self.handle_api_error(
            APIError(ErrorCodes.NO_SUCH_RESOURCE, "Not found"))

    def _parse_native_tag(self, file_id: int) -> HTTPResponse:
        result = self.controller.pase_native_tag(file_id)

        if isinstance(result, APIError):
            return self.handle_api_error(result)

        return HTTPResponse(HTTPResponseCode.OK, TagFormatter.format(result))

    def _parse_tags(self, file_id: int, sources: str) -> HTTPResponse:
        result = self.controller.pase_tags(file_id)

        if isinstance(result, APIError):
            return self.handle_api_error(result)

        return HTTPResponse(HTTPResponseCode.OK, TagFormatter.format(result))

    def _get_tag_state(self, tag_id: int) -> HTTPResponse:
        result = self.controller.get_tag_state(tag_id)

        if isinstance(result, APIError):
            return self.handle_api_error(result)

        return HTTPResponse(HTTPResponseCode.OK, TagStateFormatter.format(result))

    def _get_tags(self, file_id: int) -> HTTPResponse:
        result = self.controller.get_tags(file_id)

        if isinstance(result, APIError):
            return self.handle_api_error(result)

        return HTTPResponse(HTTPResponseCode.OK, TagFormatter.format_list(result))

    def _get_apic(self, request: AuthorizedHTTPRequest) -> HTTPResponse:
        try:
            url = FileURLParser.parse(request.json_payload)
        except KeyError:
            return self.handle_api_error(
                APIError(
                    ErrorCodes.BAD_ARGUMENT,
                    "Failed to parse request body"))

        result = self.controller.get_apic(url)

        if isinstance(result, APIError):
            return self.handle_api_error(result)

        return HTTPResponse(HTTPResponseCode.OK, None, apic=result)

    def _create_tag_mapping(self, file_id: int) -> HTTPResponse:
        result = self.controller.create_tag_mapping(file_id)

        if isinstance(result, APIError):
            return self.handle_api_error(result)

        return HTTPResponse(HTTPResponseCode.OK, TagMappingFormatter.format(result))

    def _get_tag_mapping_by_file(self, file_id: int) -> HTTPResponse:
        pass

    def _get_tag_mapping(self, mapping_id: int) -> HTTPResponse:
        pass

    def _update_tag_mapping(self, request: AuthorizedHTTPRequest) -> HTTPResponse:
        pass
