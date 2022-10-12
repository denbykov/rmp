from source.Business.Entities.File.FileSourceInfo import *


class URLFormatter:
    # Todo: Move it back to the presentation layer with access though the same factory
    @staticmethod
    def format(info: FileSourceInfo) -> str:

        if info.source == FileSource.YOUTUBE:
            return URLFormatter.format_yt_url(info.uid)

        raise RuntimeError("Unknown file source")

    @staticmethod
    def format_yt_url(uid: str) -> str:
        return f"https://www.youtube.com/watch?v={uid}"

    @staticmethod
    def format_yt_oembed_json_url(uid: str) -> str:
        return \
            f"https://www.youtube.com/oembed?format=json&url=https%3A%2F%2F" \
            f"www.youtube.com%2Fwatch%3Fv%3D{uid}"

    @staticmethod
    def format_itunes_music_search_url(artist: str, title: str) -> str:
        return \
            f'https://itunes.apple.com/search?' \
            f'term={"+".join(artist.split(" "))}+{"+".join(title.split(" "))}' \
            f'&media=music' \
            f'&limit=1'

    @staticmethod
    def format_spotify_music_search_url(
            artist: str,
            title: str,
            limit: int) -> str:
        return \
            f'https://api.spotify.com/v1/search?q=artist%3A' \
            f'{artist.replace(" ", "%20")}' \
            f'%20track%3A{title.replace(" ", "%20")}' \
            f'&type=track' \
            f'&limit={limit}'
