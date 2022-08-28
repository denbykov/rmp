from .IWebParser import *

from source.Business.Entities.Tag.TagSource import *


class IWebParserFactory(ABC):
    @abstractmethod
    def create_parser(self, source: TagSourceName) -> IWebParser:
        pass
