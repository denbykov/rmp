from source.Business.IFileAccessor import *


class FileAccessorMock(IFileAccessor):
    def read_file(self, file: pathlib.Path) -> bytes:
        pass

    def write_file(self, file: pathlib.Path, data: bytes):
        pass

    def make_dir(self, dir: pathlib.Path):
        pass

    def exists(self, path: pathlib.Path):
        pass

    def apply_tag(self, data: bytes, tag: Tag):
        pass
