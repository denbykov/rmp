from source.Business.IFileAccessor import IFileAccessor
from source.Business.TagManagement.IWebParser import *
from .SeleniumGoogleSearchResponseParser import *

from source.Business.IBrowser import IBrowser

import logging
import source.LoggerNames as LoggerNames

from source.LogContext import *

from source.Business.URLFormatter import URLFormatter
from source.Business.URLParser import URLParser


class SeleniumGoogleSearchWebParser(IWebParser):
    def __init__(
            self,
            browser: IBrowser,
            file_accessor: IFileAccessor):
        self.browser: IBrowser = browser
        self.logger: logging.Logger = logging.getLogger(LoggerNames.BUSINESS)
        self.response_parser: SeleniumGoogleSearchResponseParser = \
            SeleniumGoogleSearchResponseParser()
        self.file_accessor: IFileAccessor = file_accessor

    def parse(
            self,
            tag: Tag,
            primary_data: Union[str, Tag],
            lock: threading.Lock,
            progress: ParsingProgress) -> Tag:
        parsing_succeeded: bool = False

        try:
            if not parsing_succeeded:
                parsing_succeeded = self._parse(tag, primary_data)
        except Exception as ex:
            self.logger.error(
                LogContext.form(self) + " Web Parsing Error - " + str(ex))
            with lock:
                progress.state = TagStateName.ERROR

        if parsing_succeeded:
            with lock:
                progress.state = TagStateName.READY

        else:
            self.logger.error(
                LogContext.form(self) + " Parsing Failed With No Distinct Error")
            with lock:
                progress.state = TagStateName.ERROR

        return tag

    def _parse(self, tag: Tag, native_tag: Tag) -> bool:
        self.browser.locate_to_page(
            URLFormatter.format_google_search_url(
                native_tag.artist,
                native_tag.name))

        self.browser.click_element(
            "//span[@class='b0Xfjd' and text()='Lyrics']/parent::*")

        data: List[str] = list()

        data.append(self.browser.get_text_of_element(
            "//div[@aria-level='2' and @role='heading' and text()='Lyrics']"
            "/parent::*/parent::*/parent::*"))
        data.append(self.browser.get_text_of_element(
            "//div[@aria-level='2' and @role='heading' and text()='About']"
            "/parent::*/parent::*/parent::*"))

        result: TagParsingResult = self.response_parser.parse(tag, data)
        tag = result.tag
        tag.name = native_tag.name
        tag.apic_path = ""

        return True
