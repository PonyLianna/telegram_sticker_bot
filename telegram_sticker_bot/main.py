#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

import logging

from telegram import __version__ as TG_VER, InlineKeyboardMarkup, InlineKeyboardButton

from telegram_sticker_bot.commands import echo, get_set, start, sticker, user_info
from telegram_sticker_bot.config import Configuration

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
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    CommandHandler,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


def main() -> None:
    config = Configuration().data
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(config["bot"]["token"]).build()

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(filters.ATTACHMENT, sticker))

    application.add_handler(CallbackQueryHandler(get_set))
    application.add_handler(CommandHandler(config["commands"]["user_info"], user_info))
    application.add_handler(CommandHandler(config["commands"]["start"], start))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
