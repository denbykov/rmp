import pathlib

from source.Business.IFileAccessor import IFileAccessor


class FileAccessor(IFileAccessor):
    def read_file(self, file: pathlib.Path) -> bytes:
        with open(file, "rb") as file_obj:
            data = file_obj.read()
        return data

    def write_file(self, file: pathlib.Path, data: bytes):
        with open(file, "wb") as file_obj:
            file_obj.write(data)
