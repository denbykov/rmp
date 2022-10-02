from source.Business.Entities.Tag.TagMapping import *
from .TagSourceParser import *

from typing import *


class TagMappingParser:
    @staticmethod
    def parse(mapping: Dict[str, Any]) -> TagMapping:
        return TagMapping(
            id=mapping["id"],
            file_id=mapping["fileId"],
            name=TagSourceParser.parse(mapping["name"]),
            artist=TagSourceParser.parse(mapping["artist"]),
            lyrics=TagSourceParser.parse(mapping["lyrics"]),
            year=TagSourceParser.parse(mapping["year"]),
            apic=TagSourceParser.parse(mapping["apic"])
        )
