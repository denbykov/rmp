from source.Business.TagManagement.IWebParser import *
from source.Business.IBrowser import *

from source.Presentation.Formatters.URLFormatter import *

from bs4 import BeautifulSoup
import bs4.element

import logging
import source.LoggerNames as LoggerNames

from source.LogContext import *


class NativeYoutubeParser(IWebParser):
    def __init__(self, browser: IBrowser):
        self.browser: IBrowser = browser
        self.logger: logging.Logger = logging.getLogger(LoggerNames.DATA)

    def parse(
            self,
            tag: Tag,
            primary_data: Union[str, Tag],
            lock: threading.Lock,
            progress: ParsingProgress) -> Tag:
        try:
            page_content = self.browser.get_page_content(
                URLFormatter.format_yt_url(primary_data))

            soup: BeautifulSoup = BeautifulSoup(page_content, 'html.parser')

            tag.name = self.parse_name(soup)
        except Exception as ex:
            self.logger.error(
                LogContext.form(self) + " Web Parsing Error - " + str(ex))
            with lock:
                progress.state = TagStateName.ERROR

        with lock:
            progress.state = TagStateName.READY

    @staticmethod
    def parse_name(soup: BeautifulSoup):
        name_header: bs4.element.Tag = soup.find(
            "h1", class_="title style-scope ytd-video-primary-info-renderer")
        return name_header.text
