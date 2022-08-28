from source.Business.TagManagement.IParsingManager import *


class ParsingManagerMock(IParsingManager):
    def run(self) -> None:
        pass

    def enqueue_tag(self, tag: Tag):
        pass

    def enqueue_native_tag(self, tag: Tag, uid: str):
        pass

    def get_progress(self, tag_id: int) -> Optional[Tuple[ParsingProgress, Tag]]:
        pass

    def del_progress(self, tag_id: int):
        pass
