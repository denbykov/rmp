from typing import Optional

from .Tag.Tag import *

from dataclasses import dataclass


@dataclass
class TagParsingResult:
    tag: Tag
    apic_url: Optional[str]
