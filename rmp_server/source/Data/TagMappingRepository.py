import sqlite3

from source.Business.Entities.Tag.TagMapping import *

import logging
import source.LoggerNames as LoggerNames
from source.LogContext import *

from .utils import *

SELECT_TAG_MAPPING_FROM_TAG_MAPPING: str = \
    "select " \
    "tm.id," \
    "tm.fileId," \
    "ts_name.id, ts_name.name," \
    "ts_artist.id, ts_artist.name," \
    "ts_lyrics.id, ts_lyrics.name," \
    "ts_year.id, ts_year.name," \
    "ts_apic.id, ts_apic.name," \
    "from TagMapping tm" \
    "inner join TagSource ts_name on ts_name.id = tm.name" \
    "inner join TagSource ts_artist on ts_artist.id = tm.artist" \
    "inner join TagSource ts_lyrics on ts_lyrics.id = tm.lyrics" \
    "inner join TagSource ts_year on ts_year.id = tm.year" \
    "inner join TagSource ts_apic on ts_apic.id = tm.apic"


class TagMappingRepository:
    def __init__(self):
        self.logger: logging.Logger = logging.getLogger(LoggerNames.DATA)

    @staticmethod
    def parse_tag_source(row, idx: int) -> TagSource:
        return TagSource(
            id=row[idx],
            name=row[idx + 1]
        )

    @staticmethod
    def parse_tag_mapping(row) -> TagMapping:
        return TagMapping(
            id=row[0],
            file_id=row[1],
            name=TagMappingRepository.parse_tag_source(row, 2),
            artist=TagMappingRepository.parse_tag_source(row, 4),
            lyrics=TagMappingRepository.parse_tag_source(row, 6),
            year=TagMappingRepository.parse_tag_source(row, 8),
            apic=TagMappingRepository.parse_tag_source(row, 10)
        )

    def add_mapping(self, mapping: TagMapping, con: sqlite3.Connection) \
            -> Tuple[DataError, TagMapping]:
        try:
            with con:
                cursor: sqlite3.Cursor = con.execute(
                    "insert into "
                    "TagMapping(fileId,name,artist,lyrics,year,apic) "
                    "values ((?),(?),(?),(?),(?),(?))",
                    (mapping.file_id, mapping.name.id, mapping.artist.id,
                     mapping.lyrics.id, mapping.year.id, mapping.apic.id))
                con.commit()

                mapping.id = cursor.lastrowid

                return make_da_response(result=mapping)
        except sqlite3.IntegrityError as ex:
            return make_da_response(error=ErrorCodes.RESOURCE_ALREADY_EXISTS)
        except sqlite3.OperationalError as ex:
            self.logger.error(LogContext.form(self) + " - " + str(ex))
            return make_da_response(error=ErrorCodes.UNKNOWN_ERROR)

    def update_mapping(
            self,
            mapping: TagMapping,
            con: sqlite3.Connection) \
            -> Tuple[DataError, None]:
        try:
            query = \
                "update TagMapping" \
                " set fileId = (?)," \
                " name = (?)," \
                " artist = (?)," \
                " lyrics = (?)," \
                " year = (?)," \
                " apic = (?)" \
                f" where id = (?)"

            with con:
                con.execute(
                    query,
                    (mapping.file_id,
                     mapping.name.id,
                     mapping.artist.id,
                     mapping.lyrics.id,
                     mapping.year.id,
                     mapping.apic.id,
                     mapping.id))
                con.commit()
                return make_da_response(result=None)
        except sqlite3.IntegrityError as ex:
            return make_da_response(error=ErrorCodes.NO_SUCH_RESOURCE)
        except sqlite3.OperationalError as ex:
            self.logger.error(LogContext.form(self) + " - " + str(ex))
            return make_da_response(error=ErrorCodes.UNKNOWN_ERROR)

    def get_mapping(
            self,
            mapping_id: int,
            con: sqlite3.Connection) \
            -> Tuple[DataError, TagMapping]:
        try:
            with con:
                query = \
                    SELECT_TAG_MAPPING_FROM_TAG_MAPPING + \
                    "where TagMapping.id = (?)"

                rows = con.execute(query, (mapping_id,)).fetchall()

                if not rows:
                    return make_da_response(error=ErrorCodes.NO_SUCH_RESOURCE)
                result = self.parse_tag_mapping(rows)

                return make_da_response(result=result)
        except sqlite3.OperationalError as ex:
            self.logger.error(LogContext.form(self) + " - " + str(ex))
            return make_da_response(error=ErrorCodes.UNKNOWN_ERROR)

    def get_mapping_by_file(
            self,
            file_id: int,
            con: sqlite3.Connection) \
            -> Tuple[DataError, TagMapping]:
        try:
            with con:
                query = \
                    SELECT_TAG_MAPPING_FROM_TAG_MAPPING + \
                    "where TagMapping.fileId = (?)"

                rows = con.execute(query, (file_id,)).fetchall()

                if not rows:
                    return make_da_response(error=ErrorCodes.NO_SUCH_RESOURCE)
                result = self.parse_tag_mapping(rows)

                return make_da_response(result=result)
        except sqlite3.OperationalError as ex:
            self.logger.error(LogContext.form(self) + " - " + str(ex))
            return make_da_response(error=ErrorCodes.UNKNOWN_ERROR)
