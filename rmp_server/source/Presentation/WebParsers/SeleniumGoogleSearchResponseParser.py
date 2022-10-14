import logging

import source.LoggerNames as LoggerNames
from source.Business.Entities.Tag.Tag import Tag
from source.Presentation.WebParsers.TagParsingResult import TagParsingResult

from typing import *

from datetime import datetime


class SeleniumGoogleSearchResponseParser:
    def __init__(self):
        self.logger: logging.Logger = logging.getLogger(LoggerNames.PRESENTATION)

    def parse(
            self,
            tag: Tag,
            data: List[str]) -> TagParsingResult:
        apic_url = ""

        lyrics_container: str = data[0]
        tag.lyrics = "\n".join(
            self._remove_source_from_lyrics(lyrics_container.split("\n")[1:-1])
        )

        about_container: str = data[1]

        for el in about_container.split("\n"):
            if el.find(":") != -1:
                splitted_element = el.split(":")
                if splitted_element[0] == "Artist":
                    tag.artist = splitted_element[1]
                if splitted_element[0] == "Released":
                    tag.year = int(splitted_element[1])
                # if splitted_element[0] == "Album":
                #     tag.album = splitted_element[1]

        return TagParsingResult(tag, apic_url)

    def _remove_source_from_lyrics(self, data: List[str]) -> List[str]:
        result: List[str] = list()
        for el in data:
            if el.find("Source: ") != -1:
                break
            result.append(el)
        return result

