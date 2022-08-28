from .TagSource import *
from .TagState import *

from dataclasses import dataclass

from pathlib import Path


@dataclass
class Tag:
    id: int
    file_id: int
    source: TagSource
    state: TagState
    name: str
    artist: str
    lyrics: str
    year: int
    apic_path: Path
