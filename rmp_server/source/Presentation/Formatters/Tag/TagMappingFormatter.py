from source.Business.Entities.Tag.TagMapping import *
from .TagSourceFormatter import *

from typing import *


class TagMappingFormatter:
    @staticmethod
    def format(mapping: TagMapping) -> Dict[str, Any]:
        return {
            "id": mapping.id,
            "fileId": mapping.file_id,
            "name": TagSourceFormatter.format(mapping.name),
            "artist": TagSourceFormatter.format(mapping.artist),
            "lyrics": TagSourceFormatter.format(mapping.lyrics),
            "year": TagSourceFormatter.format(mapping.year),
            "apic": TagSourceFormatter.format(mapping.apic),
        }
