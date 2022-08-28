from source.Business.Entities.Tag.TagState import *

from typing import *


class TagStateFormatter:
    @staticmethod
    def format(state: TagState) -> Dict[str, Any]:
        return {"name": state.name.value}
