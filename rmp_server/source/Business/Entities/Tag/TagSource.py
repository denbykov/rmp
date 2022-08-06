from enum import Enum

from dataclasses import dataclass


class TagSourceName(Enum):
    NATIVE = "native"
    SPOTIFY = "spotify"
    ITUNES = "itunes"
    CELERIS_GOOGLE_SEARCH = "celeris-google-search"

    def get_abbreviation(self) -> str:
        if self.value == self.NATIVE.value:
            return "nt"
        if self.value == self.SPOTIFY.value:
            return "st"
        if self.value == self.ITUNES.value:
            return "it"
        if self.value == self.CELERIS_GOOGLE_SEARCH.value:
            return "cgs"


@dataclass
class TagSource:
    id: int
    name: TagSourceName
