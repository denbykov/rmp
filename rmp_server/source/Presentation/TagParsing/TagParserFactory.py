from source.Business.TagManagement.ITagParserFactory import *

from .NativeYoutubeParser import *
from .ItunesParser import *


class TagParserFactory(ITagParserFactory):
    def create(self, source: TagSourceName) -> ITagParser:
        if source == TagSourceName.NATIVE_YT:
            return NativeYoutubeParser()

        if source == TagSourceName.ITUNES:
            return ItunesParser()

        raise RuntimeError(f"Failed to create parser for {source}")
