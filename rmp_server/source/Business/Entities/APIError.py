from dataclasses import dataclass
from enum import Enum


class ErrorCodes(Enum):
    RESOURCE_ALREADY_EXISTS = 1
    UNKNOWN_ERROR = 2
    NO_SUCH_RESOURCE = 3
    UNAUTHORIZED = 4
    UNEXPECTED_ARGUMENT = 5
    BAD_ARGUMENT = 6
    PREREQUISITES_ARENT_MET = 7


@dataclass
class APIError:
    code: ErrorCodes
    msg: str
