from source.Business.Entities.File.FileSourceInfo import *

import re


class URLParser:
    @staticmethod
    def parse(url: str) -> FileSourceInfo:
        url = url.replace("https://www.", "")
        url = url.replace("https://", "")

        if url.startswith("youtube.com"):
            return URLParser._parse_regular_yt_url(url)
        if url.startswith("youtu.be"):
            return URLParser._parse_share_yt_url(url)

        raise RuntimeError("Unknown file source")

    @staticmethod
    def _parse_regular_yt_url(url: str) -> FileSourceInfo:
        uid = re.search("\?v=[^&]*&", url).group()[3:-1]
        return FileSourceInfo(FileSource.YOUTUBE, uid)

    @staticmethod
    def _parse_share_yt_url(url: str) -> FileSourceInfo:
        uid = re.search("be/.*", url).group()[3:]
        return FileSourceInfo(FileSource.YOUTUBE, uid)

