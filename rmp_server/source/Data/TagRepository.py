import sqlite3

from source.Business.Entities.Tag.Tag import *

import logging
import source.LoggerNames as LoggerNames
from source.LogContext import *

from .utils import *

SELECT_TAG_FROM_TAG: str =\
    "select " \
    "Tag.id," \
    "Tag.fileId," \
    "TagSource.id,TagSource.name," \
    "TagState.id,TagState.name," \
    "Tag.name, Tag.artist, Tag.lyrics, Tag.year, Tag.apicPath from Tag "


class TagRepository:
    def __init__(self):
        self.logger: logging.Logger = logging.getLogger(LoggerNames.DATA)

    @staticmethod
    def parse_tag(row) -> Tag:
        return Tag(
            id=row[0],
            file_id=row[1],
            source=TagSource(
                id=row[2],
                name=TagSourceName(row[3])),
            state=TagState(
                id=row[4],
                name=TagStateName(row[5])),
            name=row[6],
            artist=row[7],
            lyrics=row[8],
            year=row[9],
            apic_path=Path(row[10])
        )

    def get_tag_sources(self, con: sqlite3.Connection) \
            -> Tuple[DataError, Dict[TagSourceName, int]]:
        try:
            with con:
                rows = con.execute("select * from TagSource").fetchall()
                if rows:
                    result = dict()

                    for row in rows:
                        result[TagSourceName(row[1])] = row[0]

                    return make_da_response(result=result)
                else:
                    return make_da_response(error=ErrorCodes.NO_SUCH_RESOURCE)
        except sqlite3.OperationalError as ex:
            self.logger.error(LogContext.form(self) + " - " + str(ex))
            return make_da_response(error=ErrorCodes.UNKNOWN_ERROR)

    def get_tag_states(self, con: sqlite3.Connection) \
            -> Tuple[DataError, Dict[TagStateName, int]]:
        try:
            with con:
                rows = con.execute("select * from TagState").fetchall()
                if rows:
                    result = dict()

                    for row in rows:
                        result[TagStateName(row[1])] = row[0]

                    return make_da_response(result=result)
                else:
                    return make_da_response(error=ErrorCodes.NO_SUCH_RESOURCE)
        except sqlite3.OperationalError as ex:
            self.logger.error(LogContext.form(self) + " - " + str(ex))
            return make_da_response(error=ErrorCodes.UNKNOWN_ERROR)

    def add_tag(self, tag: Tag, con: sqlite3.Connection) \
            -> Tuple[DataError, Tag]:
        try:
            with con:
                cursor: sqlite3.Cursor = con.execute(
                    "insert into "
                    "Tag(fileId,sourceId,stateId,name,artist,lyrics,year,apicPath) "
                    "values ((?),(?),(?),(?),(?),(?),(?),(?))",
                    (tag.file_id, tag.source.id, tag.state.id, tag.name,
                     tag.artist, tag.lyrics, tag.year, str(tag.apic_path)))
                con.commit()

                tag.id = cursor.lastrowid

                return make_da_response(result=tag)
        except sqlite3.IntegrityError as ex:
            return make_da_response(error=ErrorCodes.RESOURCE_ALREADY_EXISTS)
        except sqlite3.OperationalError as ex:
            self.logger.error(LogContext.form(self) + " - " + str(ex))
            return make_da_response(error=ErrorCodes.UNKNOWN_ERROR)

    def get_tags_by_state(self, states: Tuple[TagStateName, ...], con: sqlite3.Connection) \
            -> Tuple[DataError, List[Tag]]:
        try:
            if len(states) == 0:
                return make_da_response(error=ErrorCodes.UNEXPECTED_ARGUMENT)

            qlist = QueryList(states, lambda state: state.value).resolve()

            query = \
                SELECT_TAG_FROM_TAG + \
                "inner join TagState on TagState.id=Tag.stateId " \
                "inner join TagSource on TagSource.id=Tag.sourceId " \
                f"where TagState.name in " \
                f"{qlist}"

            self.logger.info(query)

            with con:
                rows = con.execute(query).fetchall()
                result = list()

                for row in rows:
                    tag = self.parse_tag(row)

                    result.append(tag)

                return make_da_response(result=result)
        except sqlite3.OperationalError as ex:
            self.logger.error(LogContext.form(self) + " - " + str(ex))
            return make_da_response(error=ErrorCodes.UNKNOWN_ERROR)

    def update_tag_state(self, tag_id: int, state: TagState, con: sqlite3.Connection) \
            -> Tuple[DataError, None]:
        try:
            query = \
                "update Tag " \
                "set stateId = (?)" \
                f"where id = (?)"

            with con:
                con.execute(query, (state.id, tag_id))
                con.commit()
                return make_da_response(result=None)
        except sqlite3.IntegrityError as ex:
            return make_da_response(error=ErrorCodes.NO_SUCH_RESOURCE)
        except sqlite3.OperationalError as ex:
            self.logger.error(LogContext.form(self) + " - " + str(ex))
            return make_da_response(error=ErrorCodes.UNKNOWN_ERROR)

    def update_tag(self, tag: Tag, con: sqlite3.Connection) \
            -> Tuple[DataError, None]:
        try:
            query = \
                "update Tag " \
                "set fileId = (?)," \
                " sourceId = (?)," \
                " stateId = (?)," \
                " name = (?)," \
                " artist = (?)," \
                " lyrics = (?)," \
                " year = (?)," \
                " apicPath = (?)" \
                f" where id = (?)"

            with con:
                con.execute(
                    query,
                    (tag.file_id, tag.source.id, tag.state.id, tag.name,
                     tag.artist, tag.lyrics, tag.year, str(tag.apic_path), tag.id))
                con.commit()
                return make_da_response(result=None)
        except sqlite3.IntegrityError as ex:
            return make_da_response(error=ErrorCodes.NO_SUCH_RESOURCE)
        except sqlite3.OperationalError as ex:
            self.logger.error(LogContext.form(self) + " - " + str(ex))
            return make_da_response(error=ErrorCodes.UNKNOWN_ERROR)

    def get_tag(self, tag_id: int, con: sqlite3.Connection) -> Tuple[DataError, Tag]:
        try:
            with con:
                query = \
                    SELECT_TAG_FROM_TAG + \
                    "inner join TagState on TagState.id=Tag.stateId " \
                    "inner join TagSource on TagSource.id=Tag.sourceId " \
                    "where Tag.id = (?)"

                rows = con.execute(query, (tag_id,)).fetchall()

                if not rows:
                    return make_da_response(error=ErrorCodes.NO_SUCH_RESOURCE)
                result = self.parse_tag(rows[0])

                return make_da_response(result=result)
        except sqlite3.OperationalError as ex:
            self.logger.error(LogContext.form(self) + " - " + str(ex))
            return make_da_response(error=ErrorCodes.UNKNOWN_ERROR)

    def get_native_tag_for_file(
            self,
            file_id: int,
            native_tag_sources: Tuple[int],
            con: sqlite3.Connection) -> Tuple[DataError, Tag]:
        try:
            with con:
                qlist = QueryList(
                    native_tag_sources,
                    lambda source_id: source_id).resolve()

                query = \
                    SELECT_TAG_FROM_TAG + \
                    f"inner join TagState on TagState.id=Tag.stateId " \
                    f"inner join TagSource on TagSource.id=Tag.sourceId " \
                    f"where Tag.fileId=(?) and Tag.sourceId in {qlist}"

                rows = con.execute(query, (file_id,)).fetchall()

                if not rows:
                    return make_da_response(error=ErrorCodes.NO_SUCH_RESOURCE)
                result = self.parse_tag(rows[0])

                return make_da_response(result=result)
        except sqlite3.OperationalError as ex:
            self.logger.error(LogContext.form(self) + " - " + str(ex))
            return make_da_response(error=ErrorCodes.UNKNOWN_ERROR)

    def get_tags(
            self,
            file_id: int,
            con: sqlite3.Connection) -> Tuple[DataError, List[Tag]]:
        try:
            with con:
                query = \
                    SELECT_TAG_FROM_TAG + \
                    "inner join TagState on TagState.id=Tag.stateId " \
                    "inner join TagSource on TagSource.id=Tag.sourceId " \
                    "where Tag.fileId = (?)"

                rows = con.execute(query, (file_id,)).fetchall()

                if not rows:
                    return make_da_response(error=ErrorCodes.NO_SUCH_RESOURCE)
                result = list()
                for row in rows:
                    result.append(self.parse_tag(row))

                return make_da_response(result=result)
        except sqlite3.OperationalError as ex:
            self.logger.error(LogContext.form(self) + " - " + str(ex))
            return make_da_response(error=ErrorCodes.UNKNOWN_ERROR)
