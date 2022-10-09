from typing import *


class RequestURLParser:
    @staticmethod
    def get_option(url: str, option: str) -> List[str]:
        name_spos = url.find("?")
        return RequestURLParser._get_option(url, option, name_spos)

    @staticmethod
    def _get_option(url: str, option: str, spos: int) -> List[str]:
        result = list()

        name_spos = spos + 1
        name_epos = url.find("=", spos)

        if name_spos == -1 or name_epos == -1:
            return result

        value_spos = name_epos + 1
        value_epos = url.find("&", name_epos)
        if value_epos == -1:
            value_epos = len(url)

        if option == url[name_spos:name_epos]:
            result.append(url[value_spos:value_epos])

        others = RequestURLParser._get_option(url, option, value_epos)
        result.extend(others)

        return result

    @staticmethod
    def option_to_bool(opt: str) -> bool:
        if opt == "true":
            return True
        return False
