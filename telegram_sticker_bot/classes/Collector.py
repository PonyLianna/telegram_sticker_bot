from typing import List

from telegram import File

from telegram_sticker_bot.helpers import convert_webm_bytes_to_mp4_bytes, webp_to_bytes


class Collector:
    def __init__(self, webp: List["File"], webm: List["File"]):
        self._webp: List["File"] = webp
        self._webm: List["File"] = webm

    async def webp_to(self, format="PNG") -> List[bytes]:
        return [webp_to_bytes(await i.download_as_bytearray(), format) for i in self._webp]

    async def webm_to_mp4(self) -> List[bytes]:
        return [convert_webm_bytes_to_mp4_bytes(await i.download_as_bytearray()) for i in self._webm]

    @property
    def webp(self):
        return self._webp

    @property
    def webm(self):
        return self._webm

    @classmethod
    def collect_and_filter(cls, str_lst: List["File"]):
        webp_files: List["File"] = []
        webm_files: List["File"] = []

        for i in str_lst:
            if i.file_path.endswith(".webp"):
                webp_files.append(i)
            elif i.file_path.endswith(".webm"):
                webm_files.append(i)

        return cls(webp=webp_files, webm=webm_files)
