from source.Business.TagManagement.IWebParser import *
from source.Business.IBrowser import *
from source.Business.IRequestAgent import *

from source.Presentation.Formatters.URLFormatter import *

from bs4 import BeautifulSoup
import bs4.element

import string
import re

import logging
import source.LoggerNames as LoggerNames

from source.LogContext import *

BANNED_PHRASES: List = [
    " - Topic"]

BANNED_NAME_PHRASES_IN_PARENTHESES: List = [
    "Official Music Video", "Unofficial Videoclip", "official video", ""]


class NativeYoutubeParser(IWebParser):
    def __init__(self, browser: IBrowser, agent: IRequestAgent):
        self.browser: IBrowser = browser
        self.request_agent: IRequestAgent = agent
        self.logger: logging.Logger = logging.getLogger(LoggerNames.PRESENTATION)
        self.name_cleaning_regex = self.construct_name_cleaning_regex(
            BANNED_PHRASES,
            BANNED_NAME_PHRASES_IN_PARENTHESES)
        self.artist_cleaning_regex = self.construct_artist_cleaning_regex(
            BANNED_PHRASES)

    def parse(
            self,
            tag: Tag,
            primary_data: Union[str, Tag],
            lock: threading.Lock,
            progress: ParsingProgress) -> Tag:
        parsing_succeeded: bool = False

        try:
            if not parsing_succeeded:
                parsing_succeeded = self.parse_oembed_data(tag, primary_data)
        except Exception as ex:
            self.logger.error(
                LogContext.form(self) + " Web Parsing Error - " + str(ex))
            with lock:
                progress.state = TagStateName.ERROR

        if parsing_succeeded:
            with lock:
                progress.state = TagStateName.READY

        else:
            self.logger.error(
                LogContext.form(self) + " Parsing Failed With No Error")
            with lock:
                progress.state = TagStateName.ERROR

        return tag

    def parse_oembed_data(self, tag: Tag, url: str) -> bool:
        code, data = self.request_agent.read_json(
            URLFormatter.format_yt_oembed_json_url(url))

        if code != 200:
            return False

        name, artist =\
            self.process_primary_tags(data["title"], data["author_name"])

        tag.name = name
        tag.artist = artist

        self.download_apic(data["thumbnail_url"], tag)

        return True

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

    def download_apic(self, url: str, tag: Tag):
        code, data = self.request_agent.read_file(url)

        if code != 200:
            self.logger.error(
                LogContext.form(self) + "Failed to get image")
            return

        ext: str = url[url.rfind("."):]
        tag.apic_path = tag.apic_path.with_suffix(ext)

        with open(tag.apic_path, "wb") as file:
            file.write(data)

    # @staticmethod
    # def parse_name(soup: BeautifulSoup):
    #     name_header: bs4.element.Tag = soup.find(
    #         "h1", class_="title style-scope ytd-video-primary-info-renderer")
    #     return name_header.text

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
