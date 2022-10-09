from source.Business.IFileAccessor import IFileAccessor
from source.Business.TagManagement.IParsingDirector import *
from source.Business.TagManagement.ITagParser import *

from source.Business.IRequestAgent import IRequestAgent

import logging
import source.LoggerNames as LoggerNames

from source.LogContext import *

from source.Business.URLFormatter import URLFormatter
from source.Business.URLParser import URLParser


class NativeYoutubeDirector(IParsingDirector):
    def __init__(
            self,
            agent: IRequestAgent,
            file_accessor: IFileAccessor,
            parser: ITagParser):
        self.request_agent: IRequestAgent = agent
        self.logger: logging.Logger = logging.getLogger(LoggerNames.BUSINESS)
        self.parser: ITagParser = parser
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

    def _download_apic(self, url: str) -> Optional[bytes]:
        code, data = self.request_agent.read_file(url)

        if code != 200:
            self.logger.error(
                LogContext.form(self) + "Failed to get image")
            return None

        return data

    def _parse(self, tag: Tag, url: str) -> bool:
        code, data = self.request_agent.read_json(
            URLFormatter.format_yt_oembed_json_url(url))

        if code != 200:
            return False

        result: TagParsingResult = self.parser.parse(tag, data)
        tag = result.tag

        apic = self._download_apic(result.apic_url)
        if apic:
            ext: str = URLParser.parse_file_extension(result.apic_url)
            suffix = tag.apic_path.suffix
            tag.apic_path = tag.apic_path.with_suffix(suffix + ext)
            self.file_accessor.write_file(tag.apic_path, apic)

        return True
