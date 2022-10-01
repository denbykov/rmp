from .TagSource import *

from dataclasses import dataclass


@dataclass
class TagMapping:
    id: int
    file_id: int
    name: TagSource
    artist: TagSource
    lyrics: TagSource
    year: TagSource
    apic: TagSource
