from source.Business.TagManagement.IWebParserFactory import *
from source.Business.IRequestAgent import *
from source.Business.IBrowser import *
from source.Business.IFileAccessor import *

from .NativeYoutubeWebParser import *
from .ItunesWebParser import *
from .SpotifyWebParser import *


class WebParserFactory(IWebParserFactory):
    def __init__(
            self,
            browser: IBrowser,
            request_agent: IRequestAgent,
            file_accessor: IFileAccessor,
            spotify_api_token: str):
        self.browser = browser
        self.request_agent = request_agent
        self.spotify_api_token = spotify_api_token
        self.file_accessor = file_accessor

    def create(self, source: TagSourceName) -> IWebParser:
        if source == TagSourceName.NATIVE_YT:
            return NativeYoutubeWebParser(
                self.request_agent,
                self.file_accessor
            )

        if source == TagSourceName.ITUNES:
            return ItunesWebParser(
                self.request_agent,
                self.file_accessor
            )

        if source == TagSourceName.SPOTIFY:
            return SpotifyWebParser(
                self.request_agent,
                self.file_accessor,
                self.spotify_api_token
            )

        raise RuntimeError(f"Failed to create parser for {source}")
