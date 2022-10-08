from typing import *


class RequestURLParser:
    @staticmethod
    def get_option(url: str, option: str) -> Optional[str]:
        name_spos = url.find("?") + 1
        name_epos = url.find("=")

        if name_spos == -1 or name_epos == -1:
            return None

        if option != url[name_spos:name_epos]:
            return None

        value_spos = name_epos + 1
        value_epos = len(url)

        return url[value_spos:value_epos]
