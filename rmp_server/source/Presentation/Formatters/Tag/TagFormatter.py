from source.Business.Entities.Tag.Tag import *

from typing import *

from .TagStateFormatter import *
from .TagSourceFormatter import *


class TagFormatter:
    @staticmethod
    def format(tag: Tag) -> Dict[str, Any]:
        return {
            "id": tag.id,
            "state": TagStateFormatter.format(tag.state),
            "source": TagSourceFormatter.format(tag.source),
            "name": tag.name,
            "artist": tag.artist,
            "lyrics": tag.lyrics,
            "year": tag.year,
            "apic": str(tag.apic_path),
        }

    @staticmethod
    def format_list(tags: List[Tag]) -> List[Dict[str, Any]]:
        result = list()
        for tag in tags:
            result.append(TagFormatter.format(tag))
        return result

