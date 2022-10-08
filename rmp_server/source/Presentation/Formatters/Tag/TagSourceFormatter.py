from source.Business.Entities.Tag.TagSource import *

from typing import *


class TagSourceFormatter:
    @staticmethod
    def format(source: TagSource) -> Dict[str, Any]:
        return {
            "id": source.id,
            "name": source.name.value}

    @staticmethod
    def format_list(tags: List[TagSource]) -> List[Dict[str, Any]]:
        result = list()
        for tag in tags:
            result.append(TagSourceFormatter.format(tag))
        return result
