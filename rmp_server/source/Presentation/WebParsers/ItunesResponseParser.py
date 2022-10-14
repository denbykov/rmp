import logging

import source.LoggerNames as LoggerNames
from source.Business.Entities.Tag.Tag import Tag
from source.Presentation.WebParsers.TagParsingResult import TagParsingResult

from typing import *

from datetime import datetime


class ItunesResponseParser:
    def __init__(self):
        self.logger: logging.Logger = logging.getLogger(LoggerNames.PRESENTATION)

    def parse(
            self,
            tag: Tag,
            data: Dict,
            name: str) -> TagParsingResult:
        collection_name = data['results'][0]['collectionName']
        apic_url = ""

        if collection_name.endswith('Single'):
            tag.artist = data['results'][0]['artistName']
            tag.name = data['results'][0]['trackName']
            release_date: datetime = \
                datetime.strptime(
                    data['results'][0]['releaseDate'],
                    '%Y-%m-%dT%H:%M:%SZ')
            tag.year = int(release_date.year)
            apic_url = data['results'][0]['artworkUrl100']
        else:
            # result['album'] = collection_name
            tag.artist = data['results'][0]['artistName']
            if data['results'][0]['trackName'].lower() == name.lower():
                tag.name = data['results'][0]['trackName']
                apic_url = data['results'][0]['artworkUrl100']
                release_date: datetime = \
                    datetime.strptime(
                        data['results'][0]['releaseDate'],
                        '%Y-%m-%dT%H:%M:%SZ')
                tag.year = int(release_date.year)
                # result['number'] = data['results'][0]['trackNumber']

        return TagParsingResult(tag, apic_url)