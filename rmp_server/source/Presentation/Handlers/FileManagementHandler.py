from .AuthorizedHandler import *

from source.Presentation.Parsers.FileURLParser import *
from source.Presentation.Formatters.File.FileFormatter import *
from source.Business.Controllers.FileController import *
from source.Presentation.Parsers.RequestURLParser import RequestURLParser


class FileManagementHandler(AuthorizedHandler):
    def __init__(
            self,
            data_accessor: IDataAccessor,
            file_accessor: IFileAccessor,
            secret: str):
        super(FileManagementHandler, self).__init__(data_accessor, secret)
        self.controller: FileController = FileController(data_accessor, file_accessor)

    def authorized_handle(self, request: AuthorizedHTTPRequest) -> HTTPResponse:
        splitted_path = request.path.split('/')

        path = ""
        try:
            path = splitted_path[3]
        except IndexError:
            pass

        if path == "" and request.method == HTTPMethod.POST:
            return self._download_file(request)

        if path == "find-by-url" and request.method == HTTPMethod.POST:
            return self._find_file(request)

        if path != "":
            try:
                file_id = int(path)
                path = splitted_path[4]
                if path == "state" and request.method == HTTPMethod.GET:
                    return self._get_file_state(file_id)
                if path.startswith("data") and request.method == HTTPMethod.GET:
                    apply_tags: bool = False
                    opt = RequestURLParser.get_option(path, "applyTags")
                    if opt and opt == "true":
                        apply_tags = True
                    return self._get_file(file_id, apply_tags)
            except IndexError:
                pass

        return self.handle_api_error(
            APIError(ErrorCodes.NO_SUCH_RESOURCE, "Not found"))

    def _download_file(self, request: AuthorizedHTTPRequest) -> HTTPResponse:
        url: str = ""

        try:
            url = FileURLParser.parse(request.json_payload)
        except KeyError:
            return self.handle_api_error(
                APIError(
                    ErrorCodes.BAD_ARGUMENT,
                    "Failed to parse request body"))

        result = self.controller.download_file(url)

        if isinstance(result, APIError):
            return self.handle_api_error(result)

        return HTTPResponse(HTTPResponseCode.OK, FileFormatter.format(result))

    def _get_file_state(self, file_id: int)\
            -> HTTPResponse:
        result = self.controller.get_file_state(file_id)

        if isinstance(result, APIError):
            return self.handle_api_error(result)

        return HTTPResponse(HTTPResponseCode.OK, FileStateFormatter.format(result))

    def _get_file(self, file_id: int, apply_tags: bool)\
            -> HTTPResponse:
        result = self.controller.get_file(file_id, apply_tags)

        if isinstance(result, APIError):
            return self.handle_api_error(result)

        return HTTPResponse(HTTPResponseCode.OK, None, audio=result)

    def _find_file(self, request: AuthorizedHTTPRequest) -> HTTPResponse:
        try:
            url = FileURLParser.parse(request.json_payload)
        except KeyError:
            return self.handle_api_error(
                APIError(
                    ErrorCodes.BAD_ARGUMENT,
                    "Failed to parse request body"))

        result = self.controller.find_file(url)

        if isinstance(result, APIError):
            return self.handle_api_error(result)

        return HTTPResponse(HTTPResponseCode.OK, FileFormatter.format(result))
