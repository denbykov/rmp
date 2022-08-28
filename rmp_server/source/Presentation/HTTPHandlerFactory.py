import logging
import sqlite3

from source.Core.HTTPHandlerAdapter import IHTTPHandlerFactory
from source.Core.HTTPHandlerAdapter import IHTTPRequestHandler

from .Handlers import *

import source.LoggerNames as LoggerNames
from source.Data.DataAccerssor import DataAccessor


DB_LOCATION = "rmp_server.db"


class HTTPHandlerFactory(IHTTPHandlerFactory):
    def __init__(self, jwt_secret: str):
        self.logger = logging.getLogger(LoggerNames.PRESENTATION)
        self.jwt_secret = jwt_secret

    def create_handler(self, path: str, client: str) -> IHTTPRequestHandler:
        self.logger.info(f"{client[0]}:{client[1]}{path}")

        data_accessor = DataAccessor(sqlite3.connect(DB_LOCATION))

        if path == "/echo":
            return EchoHandler.EchoHandler(data_accessor, self.jwt_secret)
        if path == "/user":
            return UserHandler.UserHandler(data_accessor, self.jwt_secret)
        if path == '/login':
            return LoginHandler.LoginHandler(data_accessor, self.jwt_secret)
        if path.startswith('/file-management/files'):
            return FileManagementHandler.FileManagementHandler(
                data_accessor, self.jwt_secret)
        if path.startswith('/tag-management'):
            return TagManagementHandler.TagManagementHandler(
                data_accessor, self.jwt_secret)

        return NotFoundHandler.NotFoundHandler(data_accessor)
