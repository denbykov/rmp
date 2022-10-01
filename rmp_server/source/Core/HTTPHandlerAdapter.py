from .HTTPRequest import *
from .HTTPResponse import *

from http.server import BaseHTTPRequestHandler
from abc import ABC, abstractmethod

import logging
import source.LoggerNames as LoggerNames

import json
import cgi

COMMAND_GET = "GET"
COMMAND_POST = "POST"
COMMAND_PUT = "PUT"


class IHTTPRequestHandler(ABC):
    @abstractmethod
    def handle(self, request: HTTPRequest) -> HTTPResponse:
        pass


class IHTTPHandlerFactory(ABC):
    @abstractmethod
    def create_handler(self, path: str, client: tuple[str, int]) -> IHTTPRequestHandler:
        pass


class HTTPHandlerAdapter(BaseHTTPRequestHandler):
    handler_factory: IHTTPHandlerFactory
    logger = logging.getLogger(LoggerNames.CORE)
    rethrow_exceptions: bool

    @classmethod
    def attach_handler_factory(cls, handler_factory: IHTTPHandlerFactory):
        cls.handler_factory = handler_factory

    @classmethod
    def set_rethrow_exceptions(cls, rethrow_exceptions: bool):
        cls.rethrow_exceptions = rethrow_exceptions

    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

    def do_PUT(self):
        self.handle_request()

    def get_method(self) -> HTTPMethod:
        if self.command == COMMAND_GET:
            return HTTPMethod.GET

        if self.command == COMMAND_POST:
            return HTTPMethod.POST

        if self.command == COMMAND_PUT:
            return HTTPMethod.PUT

    def make_http_request(self) -> HTTPRequest:
        content_type_header = self.headers.get("content-type")
        json_payload = dict()

        if content_type_header:
            length = -1
            if self.headers.get("content-length"):
                length = int(self.headers.get("content-length"))
            content_type, options = cgi.parse_header(content_type_header)

            if content_type == "application/json":
                file: str = self.rfile.read(length).decode()
                file = file.replace("\\", "/")
                json_payload = json.loads(file)

        authorization_header = self.headers.get("Authorization")

        return HTTPRequest(self.path, self.get_method(), authorization_header, json_payload)

    def send_http_response(self, response: HTTPResponse) -> None:
        if response.json_payload:
            self.send_json_payload(
                response.json_payload, response.response_code.value)
        elif response.audio:
            self.send_file(
                response.audio, response.response_code.value, "audio", "mp3")
        elif response.apic:
            self.send_file(
                response.apic[0],
                response.response_code.value,
                "image",
                response.apic[1])
        else:
            self.send_response_only(response.response_code.value)
            self.end_headers()

    def send_json_payload(self, payload, code):
        try:
            self.send_response(code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

            body = json.dumps(payload, indent=4)
            self.wfile.write(body.encode())
        except Exception as ex:
            self.logger.error(f"Unhandled exception: {type(ex)}: {ex}")
            self.send_response_only(HTTPResponseCode.INTERNAL_ERROR.value)
            self.end_headers()

            if self.rethrow_exceptions:
                raise

    def send_file(self, payload, code, mime_type, extension):
        try:
            self.send_response(code)
            self.send_header('Content-Type', f'{mime_type}/{extension}')
            self.end_headers()
            self.wfile.write(payload)
        except Exception as ex:
            self.logger.error(f"Unhandled exception: {type(ex)}: {ex}")
            self.send_response_only(HTTPResponseCode.INTERNAL_ERROR.value)
            self.end_headers()

            if self.rethrow_exceptions:
                raise

    def handle_request(self):
        request = self.make_http_request()
        try:
            handler = self.handler_factory.create_handler(
                self.path,
                self.client_address)
            response = handler.handle(request)
            self.send_http_response(response)
        except Exception as ex:
            self.logger.error(f"Unhandled exception: {type(ex)}: {ex}")
            self.send_response_only(HTTPResponseCode.INTERNAL_ERROR.value)
            self.end_headers()

            if self.rethrow_exceptions:
                raise

    def log_message(self, format, *args):
        pass
