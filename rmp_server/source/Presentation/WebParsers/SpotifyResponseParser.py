from source.Business.Entities.Tag.Tag import Tag
from source.Presentation.WebParsers.TagParsingResult import TagParsingResult
from .NotEnoughDataException import NotEnoughDataException

from typing import *

import logging
import source.LoggerNames as LoggerNames

from datetime import datetime


class SpotifyResponseParser:
    def __init__(self):
        self.logger: logging.Logger = logging.getLogger(LoggerNames.PRESENTATION)

    def parse_item(
            self,
            tag: Tag,
            apic_url: str,
            data: Dict):
        tag.artist = data['album']['artists'][0]['name']
        tag.name = data['name']
        release_date_string = data['album']['release_date']

        release_date: datetime = \
            datetime.strptime(
                release_date_string,
                '%Y-%m-%d')
        tag.year = int(release_date.year)

        # try:
        #     tag.number = data[0]['track_number']
        # except KeyError:
        #     pass

    def parse_apic_url(
            self,
            data: Dict) -> str:
        return data['album']['images'][0]['url']

    def parse_single_item(
            self,
            tag: Tag,
            data: Dict,
            name: str) -> TagParsingResult:
        apic_url = ""

        item: Dict = data['tracks']['items'][0]

        if item['album']['album_type'] == 'album':
            if name.lower() not in item['name'].lower():
                raise NotEnoughDataException()

        self.parse_item(tag, apic_url, item)
        apic_url = self.parse_apic_url(item)

        return TagParsingResult(tag, apic_url)

    def parse_page(
            self,
            tag: Tag,
            data: Dict,
            name: str) -> TagParsingResult:
        apic_url = ""

        item: Optional[Dict] = None

        for el in data['tracks']['items']:
            if name.lower() in el['name'].lower():
                item = el
                break

        self.parse_item(tag, apic_url, item)
        apic_url = self.parse_apic_url(item)

        return TagParsingResult(tag, apic_url)
