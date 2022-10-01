from dataclasses import dataclass
from enum import Enum
from typing import *


class HTTPResponseCode(Enum):
    OK = 200
    BAD_REQUEST = 400
    INTERNAL_ERROR = 500


@dataclass
class HTTPResponse:
    response_code: HTTPResponseCode
    json_payload: Optional[Dict[str, Any]]
    audio: Optional[bytes]
    apic: Optional[Tuple[bytes, str]]

    def __init__(self, response_code, json_payload, audio=None, apic=None):
        self.response_code = response_code
        self.json_payload = json_payload
        self.audio = audio
        self.apic = apic
