from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import Update
from telegram.ext import ContextTypes
from telegram_sticker_bot.config import Configuration


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

    await update.message.reply_markdown(f"*File id:* `{sticker.file_id}`")
    await update.message.reply_markdown(f"*File Unique id:* `{sticker.file_unique_id}`")
    await update.message.reply_text(sticker_str, reply_markup=markup)
