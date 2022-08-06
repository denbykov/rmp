import sqlite3

from source.Business.Entities.File.File import *

import logging
import source.LoggerNames as LoggerNames
from source.LogContext import *

from .utils import *

SELECT_FILE_FROM_FILE: str =\
    "select " \
    "File.id,File.url,File.path," \
    "FileState.id,FileState.name,File.stateDescription from File "


class FileRepository:
    def __init__(self):
        self.logger: logging.Logger = logging.getLogger(LoggerNames.DATA)

    @staticmethod
    def parse_file(row) -> File:
        return File(
            id=row[0],
            url=row[1],
            path=row[2],
            state=FileState(
                id=row[3],
                name=FileStateName(row[4]),
                description=row[5]),
        )

    def get_file_by_url(self, url: str, con: sqlite3.Connection) -> Tuple[DataError, File]:
        try:
            query = \
                SELECT_FILE_FROM_FILE + \
                "inner join FileState on FileState.id=File.stateId " \
                "where File.url = (?)"

            with con:
                rows = con.execute(query, (url,)).fetchall()

                if not rows:
                    return make_da_response(error=ErrorCodes.NO_SUCH_RESOURCE)

                result = self.parse_file(rows[0])

                return make_da_response(result=result)
        except sqlite3.OperationalError as ex:
            self.logger.error(LogContext.form(self) + str(ex))
            return make_da_response(error=ErrorCodes.UNKNOWN_ERROR)

    def add_file(self, file: File, con: sqlite3.Connection) -> Tuple[DataError, File]:
        try:
            with con:
                cursor: sqlite3.Cursor = con.execute(
                    "insert into File(stateId,url,path,stateDescription) "
                    "values ((?),(?),(?),(?))",
                    (file.state.id, file.url, str(file.path), file.state.description))
                con.commit()

                file.id = cursor.lastrowid

                return make_da_response(result=file)
        except sqlite3.IntegrityError as ex:
            return make_da_response(error=ErrorCodes.RESOURCE_ALREADY_EXISTS)
        except sqlite3.OperationalError as ex:
            self.logger.error(LogContext.form(self) + " - " + str(ex))
            return make_da_response(error=ErrorCodes.UNKNOWN_ERROR)

    def get_file_states(self, con: sqlite3.Connection) -> Tuple[DataError, Dict[FileStateName, int]]:
        try:
            with con:
                rows = con.execute("select * from FileState").fetchall()
                if rows:
                    result = dict()

                    for row in rows:
                        result[FileStateName(row[1])] = row[0]

                    return make_da_response(result=result)
                else:
                    return make_da_response(error=ErrorCodes.NO_SUCH_RESOURCE)
        except sqlite3.OperationalError as ex:
            self.logger.error(LogContext.form(self) + " - " + str(ex))
            return make_da_response(error=ErrorCodes.UNKNOWN_ERROR)

    def get_files_by_state(self, states: Tuple[FileStateName, ...], con: sqlite3.Connection)\
            -> Tuple[DataError, List[File]]:
        try:
            if len(states) == 0:
                return make_da_response(error=ErrorCodes.UNEXPECTED_ARGUMENT)

            qlist = QueryList(states, lambda state: state.value).resolve()

            query = \
                SELECT_FILE_FROM_FILE + \
                "inner join FileState on FileState.id=File.stateId " \
                f"where FileState.name in " \
                f"{qlist}"

            self.logger.info(query)

            with con:
                rows = con.execute(query).fetchall()
                result = list()

                for row in rows:
                    file = self.parse_file(row)

                    result.append(file)

                return make_da_response(result=result)
        except sqlite3.OperationalError as ex:
            self.logger.error(LogContext.form(self) + " - " + str(ex))
            return make_da_response(error=ErrorCodes.UNKNOWN_ERROR)

    def get_file(self, file_id: int, con: sqlite3.Connection) -> Tuple[DataError, File]:
        try:
            with con:
                query = \
                    SELECT_FILE_FROM_FILE + \
                    "inner join FileState on FileState.id=File.stateId " \
                    "where File.id = (?)"

                rows = con.execute(query, (file_id,)).fetchall()

                if not rows:
                    return make_da_response(error=ErrorCodes.NO_SUCH_RESOURCE)
                result = self.parse_file(rows[0])

                return make_da_response(result=result)
        except sqlite3.OperationalError as ex:
            self.logger.error(LogContext.form(self) + " - " + str(ex))
            return make_da_response(error=ErrorCodes.UNKNOWN_ERROR)

    def update_file_state(self, file_id: int, state: FileState, con: sqlite3.Connection) -> Tuple[DataError, None]:
        try:
            query = \
                "update File " \
                "set stateId = (?)," \
                "stateDescription = (?) " \
                f"where id = (?)"

            with con:
                con.execute(query, (state.id, state.description, file_id))
                con.commit()
                return make_da_response(result=None)
        except sqlite3.IntegrityError as ex:
            return make_da_response(error=ErrorCodes.NO_SUCH_RESOURCE)
        except sqlite3.OperationalError as ex:
            self.logger.error(LogContext.form(self) + " - " + str(ex))
            return make_da_response(error=ErrorCodes.UNKNOWN_ERROR)
