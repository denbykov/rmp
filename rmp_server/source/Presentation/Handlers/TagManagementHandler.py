from .AuthorizedHandler import *

# from source.Presentation.Parsers.FileURLParser import *
from source.Presentation.Formatters.Tag.TagFormatter import *
from source.Business.Controllers.TagController import *


class TagManagementHandler(AuthorizedHandler):
    def __init__(self, data_accessor, secret: str):
        super(TagManagementHandler, self).__init__(data_accessor, secret)
        self.controller: TagController = TagController(data_accessor)

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

        if path == "tags":
            tag_id = int(splitted_path[3])
            path = splitted_path[4]

            if path == "state" and request.method == HTTPMethod.GET:
                return self._get_tag_state(tag_id)

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
