import io
from telegram import Update
from telegram.ext import ContextTypes

from telegram_sticker_bot.classes.TelegramCollector import TelegramCollector
from telegram_sticker_bot.config import Configuration

from telegram_sticker_bot.helpers import chunkify


async def get_set(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    config = Configuration().data
    callback = update.callback_query.data

    if not callback:  # empty query should not be handled
        return

    if not callback.startswith(f"/{config['commands']['get_set']}"):
        return

    sticker_set_name = callback.replace(f"/{config['commands']['get_set']}", "").strip()
    sticker_set = await update.get_bot().get_sticker_set(sticker_set_name)

    sticker_set_str = str(sticker_set)

    file_bytes = io.BytesIO(sticker_set_str.encode("utf-8"))
    file_bytes.name = f"{sticker_set_name}_telegram_sticker.txt"

    await update.get_bot().send_document(
        chat_id=update.effective_message.chat_id, document=file_bytes
    )

    await update.callback_query.answer()


async def get_set_w_images(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """POTENTIALY BUGGY!!!"""
    config = Configuration().data
    callback = update.callback_query.data

    if not callback:  # empty query should not be handled
        return

    if not callback.startswith(f"/{config['commands']['get_set_images']}"):
        return

    sticker_set_name = callback.replace(
        f"/{config['commands']['get_set_images']}", ""
    ).strip()

    sticker_set = await update.get_bot().get_sticker_set(sticker_set_name)
    telegram_collector = await TelegramCollector.create_and_collect(sticker_set)

    stickers_videos = await telegram_collector.collect_videos_docs()
    stickers_images = await telegram_collector.collect_images_docs()

    for group in chunkify(stickers_images + stickers_videos, 10):
        await update.get_bot().send_media_group(
            chat_id=update.effective_message.chat_id, media=group
        )

    await update.callback_query.answer()
