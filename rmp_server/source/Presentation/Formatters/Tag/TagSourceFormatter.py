from source.Business.Entities.Tag.TagSource import *

from typing import *


class TagSourceFormatter:
    @staticmethod
    def format(source: TagSource) -> Dict[str, Any]:
        return {
            "id": source.id,
            "name": source.name.value}
