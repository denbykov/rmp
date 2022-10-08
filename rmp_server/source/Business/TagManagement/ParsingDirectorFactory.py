from source.Business.IBrowser import IBrowser

from .ParsingDirectors.NativeYoutubeDirector import *
from .ITagParserFactory import *


class ParsingDirectorFactory:
    def __init__(
            self,
            browser: IBrowser,
            agent: IRequestAgent,
            file_accessor: IFileAccessor,
            tag_parser_factory: ITagParserFactory):
        self.browser: IBrowser = browser
        self.request_agent: IRequestAgent = agent
        self.file_accessor: IFileAccessor = file_accessor
        self.tag_parser_factory: ITagParserFactory = tag_parser_factory

    def create(self, source: TagSourceName) -> IParsingDirector:
        parser: ITagParser = self.tag_parser_factory.create(source)

        if source == TagSourceName.NATIVE_YT:
            return NativeYoutubeDirector(
                self.request_agent,
                self.file_accessor,
                parser)

        raise RuntimeError(f"Failed to create parsing director for {source}")
