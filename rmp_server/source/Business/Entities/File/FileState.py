from enum import Enum

from dataclasses import dataclass


# pay attention that database does not store "loading" and "converting" states!
# these states are temporary and set by downloader hooks
class FileStateName(Enum):
    ERROR = "error"
    PENDING = "pending"
    LOADING = "loading"
    CONVERTING = "converting"
    READY = "ready"


@dataclass
class FileState:
    id: int
    name: FileStateName
    description: str
