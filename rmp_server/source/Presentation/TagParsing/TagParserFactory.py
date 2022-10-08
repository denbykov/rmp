from source.Business.TagManagement.ITagParserFactory import *

from .NativeYoutubeParser import *


class TagParserFactory(ITagParserFactory):
    def create(self, source: TagSourceName) -> ITagParser:
        if source == TagSourceName.NATIVE_YT:
            return NativeYoutubeParser()

        raise RuntimeError(f"Failed to create parser for {source}")
