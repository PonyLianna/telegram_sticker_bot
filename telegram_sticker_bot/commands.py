import io
from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InputMediaPhoto,
)
from telegram import Update
from telegram.ext import ContextTypes

from telegram_sticker_bot.classes.Collector import Collector
from telegram_sticker_bot.config import Configuration

from telegram_sticker_bot.helpers import chunkify, webp_to_bytes


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    FOR TESTING PURPOSES
    Echo the user message.
    """
    await update.message.reply_text(update.message.text)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    config = Configuration().data
    await update.message.reply_text(config["text"]["start"])


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    config = Configuration().data
    await update.message.reply_text(config["text"]["help"])


async def user_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.from_user)


async def sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    config = Configuration().data
    sticker = update.effective_message.effective_attachment
    sticker_str = str(sticker)

    sticker_set_name = sticker.set_name
    command = f"/{config['commands']['get_set']} {sticker_set_name}"
    command_images = f"/{config['commands']['get_set_images']} {sticker_set_name}"

    inline_keyboard = [
        [
            InlineKeyboardButton(text=sticker_set_name, callback_data=command),
            InlineKeyboardButton(text=sticker_set_name, callback_data=command_images),
        ]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard)

    await update.message.reply_markdown("*File id:* `" + sticker.file_id + "`")
    await update.message.reply_markdown(
        "*File Unique id:* `" + sticker.file_unique_id + "`"
    )
    await update.message.reply_text(sticker_str, reply_markup=markup)


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
    """BUGS BE CAREFUL"""
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

    stickers_paths = [(await i.get_file()) for i in sticker_set.stickers]
    collector = Collector.collect_and_filter(stickers_paths)

    stickers_images = [InputMediaPhoto(media=bytess) for bytess in await collector.webp_to()]

    for group in chunkify(stickers_images, 10):
        await update.get_bot().send_media_group(
            chat_id=update.effective_message.chat_id, media=group
        )

    await update.callback_query.answer()
