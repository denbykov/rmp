import sqlite3

from source.Business.Entities.Tag.TagSource import *

import logging
import source.LoggerNames as LoggerNames
from source.LogContext import *

from .utils import *


class TagRepository:
    def __init__(self):
        self.logger: logging.Logger = logging.getLogger(LoggerNames.DATA)

    def get_tag_sources(self, con: sqlite3.Connection) \
            -> Tuple[DataError, Dict[TagSource, int]]:
        try:
            with con:
                rows = con.execute("select * from TagSource").fetchall()
                if rows:
                    result = dict()

                    for row in rows:
                        result[TagSource(row[1])] = row[0]

                    return make_da_response(result=result)
                else:
                    return make_da_response(error=ErrorCodes.NO_SUCH_RESOURCE)
        except sqlite3.OperationalError as ex:
            self.logger.error(LogContext.form(self) + " - " + str(ex))
            return make_da_response(error=ErrorCodes.UNKNOWN_ERROR)
