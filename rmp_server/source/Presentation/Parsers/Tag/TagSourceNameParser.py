from typing import *

from source.Business.Entities.Tag.TagSource import *


class TagSourceNameParser:
    @staticmethod
    def parse(parameter: str) -> TagSourceName:

        if parameter == TagSourceName.NATIVE_YT:
            return TagSourceName.NATIVE_YT
        if parameter == TagSourceName.SPOTIFY:
            return TagSourceName.SPOTIFY
        if parameter == TagSourceName.ITUNES:
            return TagSourceName.ITUNES
        if parameter == TagSourceName.CELERIS_GOOGLE_SEARCH:
            return TagSourceName.CELERIS_GOOGLE_SEARCH
