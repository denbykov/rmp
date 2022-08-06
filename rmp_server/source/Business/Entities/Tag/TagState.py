from enum import Enum

from dataclasses import dataclass


# pay attention that database does not store "parsing" state!
class TagStateName(Enum):
    ERROR = "error"
    PENDING = "pending"
    PARSING = "parsing"
    READY = "ready"


@dataclass
class TagState:
    id: int
    name: TagStateName
