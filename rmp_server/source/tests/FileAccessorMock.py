from source.Business.IFileAccessor import *


class FileAccessorMock(IFileAccessor):
    def read_file(self, file: pathlib.Path) -> bytes:
        pass

    def write_file(self, file: pathlib.Path, data: bytes):
        pass

    def make_dir(self, dir: pathlib.Path):
        pass
