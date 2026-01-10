from typing import List
from telegram_sticker_bot.classes.BytesName import BytesName
from telegram_sticker_bot.helpers import convert_webm_bytes_to_mp4_bytes, webp_to_bytes


class Collector:
    def __init__(self, images_lst: List["BytesName"], video_lst: List["BytesName"]):
        self._images_lst: List["BytesName"] = images_lst
        self._video_lst: List["BytesName"] = video_lst

    def webp_to(self, format="PNG") -> List[BytesName]:
        if self.images_not_empty:
            return [
                BytesName(content=webp_to_bytes(i.content, format), name=i.name)
                for i in self._images_lst
            ]
        else:
            return []

    def webm_to_mp4(self) -> List[BytesName]:
        if self.videos_not_empty:
            return [
                BytesName(
                    content=convert_webm_bytes_to_mp4_bytes(i.content), name=i.name
                )
                for i in self._video_lst
            ]
        else:
            return []

    @property
    def images(self):
        return self._images_lst

    @property
    def images_not_empty(self):
        return len(self._images_lst) > 0

    @property
    def videos(self):
        return self._video_lst

    @property
    def videos_not_empty(self):
        return len(self._video_lst) > 0
