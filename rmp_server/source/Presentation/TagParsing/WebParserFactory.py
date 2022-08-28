from source.Business.TagManagement.IWebParserFactory import *

from .WebParsers.NativeYoutubeParser import *


class WebParserFactory(IWebParserFactory):
    def __init__(self, browser: IBrowser, agent: IRequestAgent):
        self.browser: IBrowser = browser
        self.request_agent: IRequestAgent = agent

    def create_parser(self, source: TagSourceName) -> IWebParser:
        if source == TagSourceName.NATIVE_YT:
            return NativeYoutubeParser(self.browser, self.request_agent)

        raise RuntimeError(f"Failed to create tag parser for {source}")
