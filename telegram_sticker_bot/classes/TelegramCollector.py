from typing import List, Optional
from telegram import File, InputMediaDocument, InputMediaPhoto, StickerSet
from telegram_sticker_bot.classes.BytesName import BytesName
from telegram_sticker_bot.classes.Collector import Collector


class TelegramCollector:
    def __init__(self, stickerSet: "StickerSet"):
        self.sticker_set: "StickerSet" = stickerSet
        self.sticker_set_files: List["File"] = []
        self._collector: Optional["Collector"] = None

    @classmethod
    async def create_and_collect(cls, sticker_set: "StickerSet") -> "TelegramCollector":
        instance = cls(sticker_set)
        await instance.collect_and_filter()
        return instance

    async def collect_and_filter(self):
        images_lst: List[BytesName] = []
        video_lst: List[BytesName] = []

        self.sticker_set_files = [
            await sticker.get_file() for sticker in self.sticker_set.stickers
        ]

        for i in self.sticker_set_files:
            if i.file_path.endswith(".webp"):
                images_lst.append(
                    BytesName(
                        content=await i.download_as_bytearray(), name=f"{i.file_id}.png"
                    )
                )
            elif i.file_path.endswith(".webm"):
                video_lst.append(
                    BytesName(
                        content=await i.download_as_bytearray(), name=f"{i.file_id}.mp4"
                    )
                )

        self.collector = Collector(images_lst=images_lst, video_lst=video_lst)

    async def _if_not_exists_initialize(self):
        if not self.collector:
            await self.collect_and_filter()

    async def _collect_images(self) -> List[BytesName]:
        await self._if_not_exists_initialize()
        return self.collector.webp_to()

    async def _collect_videos(self) -> List[BytesName]:
        await self._if_not_exists_initialize()
        return self.collector.webm_to_mp4()

    async def collect_any_docs(
        self, collection: List[BytesName]
    ) -> List[InputMediaDocument]:
        temp_collection = []
        for i in collection:
            if i is not None:
                temp_collection.append(
                    InputMediaDocument(media=i.content, filename=i.name)
                )
        return temp_collection

    async def collect_images_docs(self) -> List[InputMediaDocument]:
        return await self.collect_any_docs(await self._collect_images())

    async def collect_images_collection(self) -> List[InputMediaPhoto]:
        return [InputMediaPhoto(media=i) for i in await self._collect_images()]

    async def collect_videos_docs(self) -> List[InputMediaDocument]:
        return await self.collect_any_docs(await self._collect_videos())

    # @classmethod
    # def collect_and_filter(cls, str_lst: List["File"]):
    #     webp_files: List["File"] = []
    #     webm_files: List["File"] = []

    #     for i in str_lst:
    #         if i.file_path.endswith(".webp"):
    #             webp_files.append(i)
    #         elif i.file_path.endswith(".webm"):
    #             webm_files.append(i)

    #     return cls(webp=webp_files, webm=webm_files)
