from dataclasses import dataclass

from .TagState import TagStateName


@dataclass
class ParsingProgress:
    state: TagStateName
