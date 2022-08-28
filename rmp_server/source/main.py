import configparser
from http.server import ThreadingHTTPServer

import logging.config
import logging.handlers

from Core.HTTPHandlerAdapter import HTTPHandlerAdapter
from Presentation.HTTPHandlerFactory import *

import source.Business.FileManagement.FileManager as fm
import source.Business.TagManagement.TagManager as tm
import source.Business.TagManagement.ParsingManager as pm

from source.Data.SeleniumBrowser import *
from source.Data.RequestAgent import *
from source.Presentation.TagParsing.WebParserFactory import *

import LoggerNames
import sqlite3

from pathlib import Path

APP_CONFIG_LOCATION = Path("config/rmp_server-config.ini")
LOGGER_CONFIG_LOCATION = Path("config/rmp_server-logging.ini")
LOG_DIR_LOCATION = Path("logs")

APP_NAME = "rmp_server"

DB_LOCATION = "rmp_server.db"


class Config:
    CORE: str = "Core"

    PORT: str = "port"
    JWT_SECRET: str = "jwt_secret"
    RETHROW_EXCEPTIONS: str = "rethrow_exceptions"

    FILE_MANAGEMENT: str = "FileManagement"

    FILE_DIR: str = "file_dir"


class ServerApplication:
    def __init__(self):
        self.config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
        self.config.read(APP_CONFIG_LOCATION)
        self.port = self.config.getint(Config.CORE, Config.PORT)
        self._init_logging()

        fm.FileManager.init(
            DataAccessor(sqlite3.connect(DB_LOCATION)),
            Path(self.config.get(Config.FILE_MANAGEMENT, Config.FILE_DIR)))

        parsing_manager: pm.ParsingManager = pm.ParsingManager(
            WebParserFactory(
                SeleniumBrowser(("--headless", "--disable-web-security")),
                RequestAgent()
            )
        )

        tm.TagManager.init(
            parsing_manager,
            DataAccessor(sqlite3.connect(DB_LOCATION)),
            Path(self.config.get(Config.FILE_MANAGEMENT, Config.FILE_DIR))
        )

    def _init_logging(self):
        if not LOG_DIR_LOCATION.is_dir():
            LOG_DIR_LOCATION.mkdir()
        self.logger = logging.getLogger(LoggerNames.APPLICATION)

        logging.config.fileConfig(LOGGER_CONFIG_LOCATION)

    def run(self):
        self.logger.info(f"Starting {APP_NAME}...")

        jwt_secret = self.config.get(Config.CORE, Config.JWT_SECRET)
        handler_factory = HTTPHandlerFactory(jwt_secret)
        HTTPHandlerAdapter.attach_handler_factory(handler_factory)

        rethrow_exceptions = self.config.getboolean(Config.CORE, Config.RETHROW_EXCEPTIONS)
        HTTPHandlerAdapter.set_rethrow_exceptions(rethrow_exceptions)

        with ThreadingHTTPServer(("", self.port), HTTPHandlerAdapter) as httpd:
            self.logger.info(f"Serving at port {self.port}")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                self.logger.info(f"Exiting...")


if __name__ == '__main__':
    app = ServerApplication()
    app.run()
