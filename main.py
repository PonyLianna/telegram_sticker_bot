#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

import logging
import os

from telegram import __version__ as TG_VER, InlineKeyboardMarkup, InlineKeyboardButton

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]
if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters, CallbackQueryHandler
import yaml

with open('./config.yaml') as f:
    config = yaml.load(f, Loader=yaml.SafeLoader)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    FOR TESTING PURPOSES
    Echo the user message.
    """
    await update.message.reply_text(update.message.text)


async def sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    sticker = update.effective_message.effective_attachment
    sticker_str = str(sticker)

    sticker_set_name = sticker.set_name
    command = f"/{config['commands']['get_set']} {sticker_set_name}"

    inline_keyboard = [[InlineKeyboardButton(text=sticker_set_name, callback_data=command)]]
    markup = InlineKeyboardMarkup(inline_keyboard)

    await update.message.reply_markdown("*File id:* `" + sticker.file_id + "`")
    await update.message.reply_markdown("*File Unique id:* `" + sticker.file_unique_id + "`")
    await update.message.reply_text(sticker_str, reply_markup=markup)


async def get_set(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    callback = update.callback_query.data

    if not callback:  # empty query should not be handled
        return

    if f"/{config['commands']['get_set']}" not in callback:
        return

    sticker_set_name = callback.replace(f"/{config['commands']['get_set']}", "").strip()
    sticker_set = await update.get_bot().get_sticker_set(sticker_set_name)
    sticker_set_str = str(sticker_set)

    file_name = f"{sticker_set_name}_telegram_sticker.txt"
    with open(file_name, "w", encoding="utf-8") as my_file:
        my_file.write(sticker_set_str)

    my_file = open(file_name, "rb")
    await update.get_bot().send_document(chat_id=update.effective_message.chat_id, document=my_file)
    await update.callback_query.answer()
    my_file.close()
    os.remove(file_name)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(config["bot"]["token"]).build()

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.ATTACHMENT, sticker))
    application.add_handler(CallbackQueryHandler(get_set))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
