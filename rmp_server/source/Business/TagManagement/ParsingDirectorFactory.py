from source.Business.IBrowser import IBrowser
from source.Business.IFileAccessor import IFileAccessor
from source.Business.IRequestAgent import IRequestAgent

from source.Business.Entities.Tag.TagSource import TagSourceName
from .ParsingDirectors.NativeYoutubeDirector import *


class ParsingDirectorFactory:
    def __init__(
            self,
            browser: IBrowser,
            agent: IRequestAgent,
            file_accessor: IFileAccessor):
        self.browser: IBrowser = browser
        self.request_agent: IRequestAgent = agent
        self.file_accessor: IFileAccessor = file_accessor

    def create(self, source: TagSourceName) -> IParsingDirector:
        if source == TagSourceName.NATIVE_YT:
            return NativeYoutubeDirector(self.request_agent, self.file_accessor)

        raise RuntimeError(f"Failed to create parsing director for {source}")
