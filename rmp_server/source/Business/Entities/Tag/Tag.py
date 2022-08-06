from .TagSource import *
from .TagState import *

from dataclasses import dataclass


@dataclass
class Tag:
    id: int
    source: TagSource
    state: TagState
