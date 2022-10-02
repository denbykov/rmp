import io
import pathlib

from source.Business.IFileAccessor import *

from mutagen.id3 import ID3, TALB, TPE1, TIT2, TORY, USLT, APIC, ID3NoHeaderError

from source.Business.URLParser import URLParser


class FileAccessor(IFileAccessor):
    def read_file(self, file: pathlib.Path) -> bytes:
        with open(file, "rb") as file_obj:
            data = file_obj.read()
        return data

    def write_file(self, file: pathlib.Path, data: bytes):
        with open(file, "wb") as file_obj:
            file_obj.write(data)

    def make_dir(self, dir: pathlib.Path):
        if not dir.is_dir():
            dir.mkdir()

    def exists(self, path: pathlib.Path):
        return path.exists()

    def apply_tag(self, data: bytes, tag: Tag, image: Optional[bytes])\
            -> bytes:
        file_stream: io.BytesIO = io.BytesIO(data)
        file: ID3
        try:
            file = ID3(file_stream)
        except ID3NoHeaderError:
            file = ID3()

        file.delete(file_stream)

        file['TIT2'] = TIT2(encoding=3, text=tag.name)
        file['TPE1'] = TPE1(encoding=3, text=tag.artist)
        # file['TALB'] = TALB(encoding=3, text=tag.album)
        file['TORY'] = TORY(encoding=3, text=str(tag.year))
        file['USLT'] = USLT(encoding=3, text=tag.lyrics)
        image_mime_type: str = \
            f'image/{URLParser.parse_file_extension(str(tag.apic_path))}'
        file.add(APIC(3, f'image/{image_mime_type}', 3, 'Front cover', image))

        file.save(file_stream)
        file_stream.seek(0, io.SEEK_SET)
        return file_stream.read()

