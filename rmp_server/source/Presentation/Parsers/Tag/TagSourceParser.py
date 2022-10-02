from source.Business.Entities.Tag.TagSource import *

from typing import *


class TagSourceParser:
    @staticmethod
    def parse(mapping: Dict[str, Any]) -> TagSource:
        return TagSource(
            id=mapping["id"],
            name=TagSourceName(mapping["name"])
        )
