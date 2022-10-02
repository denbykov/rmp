from source.Business.Entities.Tag import Tag
from source.Business.IRequestAgent import *

import string
import re

import logging
import source.LoggerNames as LoggerNames

from source.LogContext import *

BANNED_PHRASES: List = [
    " - Topic"]

BANNED_NAME_PHRASES_IN_PARENTHESES: List = [
    "Official Music Video", "Unofficial Videoclip", "official video", ""]


class NativeYoutubeParser:
    # Todo: Create interface and use it instead in a Director
    def __init__(self):
        self.logger: logging.Logger = logging.getLogger(LoggerNames.PRESENTATION)
        self.name_cleaning_regex = self.construct_name_cleaning_regex(
            BANNED_PHRASES,
            BANNED_NAME_PHRASES_IN_PARENTHESES)
        self.artist_cleaning_regex = self.construct_artist_cleaning_regex(
            BANNED_PHRASES)

    def parse(self, tag: Tag, data: Dict):
        name, artist = \
            self.process_primary_tags(data["title"], data["author_name"])

        tag.name = name
        tag.artist = artist

    def process_primary_tags(self, name: str, artist: str) -> Tuple[str, str]:
        processed_name: str = name
        processed_artist: str = None

        sep_pos = name.find('-')
        if sep_pos == -1:
            sep_pos = name.find(':')
        if sep_pos == -1:
            sep_pos = name.find('–')
        if sep_pos != -1:
            processed_name = name[sep_pos+1:]
            processed_artist = name[:sep_pos]

        if processed_artist is None:
            processed_artist = artist

        processed_name = self.clean_name(processed_name)
        processed_artist = self.clean_artist(processed_artist)

        processed_name = processed_name.strip()
        processed_artist = processed_artist.strip()

        return \
            string.capwords(processed_name), string.capwords(processed_artist)

    def clean_name(self, name: str) -> str:
        while True:
            match: re.Match = \
                re.search(self.name_cleaning_regex, name, re.IGNORECASE)
            if not match:
                break
            span: Tuple = match.span()
            name = name[:span[0]] + name[span[1]:]

        return name

    def clean_artist(self, artist: str) -> str:
        while True:
            match: re.Match = \
                re.search(self.artist_cleaning_regex, artist, re.IGNORECASE)
            if not match:
                break
            span: Tuple = match.span()
            artist = artist[:span[0]] + artist[span[1]:]

        return artist

    @staticmethod
    def construct_name_cleaning_regex(
            phrases: List[str], phrases_in_parentheses: List[str]) -> str:
        result: str = "("
        for el in phrases_in_parentheses:
            result += f"\[{el}\]|\({el}\)|"
        for el in phrases:
            result += f"{el}|"
        result = result[:-1] + ")"
        return result

    @staticmethod
    def construct_artist_cleaning_regex(phrases: List[str]) -> str:
        result: str = "("
        for el in phrases:
            result += f"{el}|"
        result = result[:-1] + ")"
        return result
