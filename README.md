# Telegram_Sticker_Bot

Simple Telegram bot for stickers debugging written on [python-telegram-bot](https://python-telegram-bot.org/)

### What it can do?

Well... It can send you _UniqueID_, or _ID_ of Sticker and StickerPack, that can help you on debugging your own sticker pack.

Right now it can also download and show you all of them in _DocumentList_ or _ImageList_.

Either it _webp_ (plain stickers) or _webm_ (animated stickers) it can group and give you a plain look on those to debug or just download.

### How to install?

Pretty simple!

`git clone https://github.com/PonyLianna/telegram_sticker_bot`

Then in the folder:

`pip install poetry`

`poetry install`

It will install all necessary requirements and you're ready to start!

#### Dealing with config

Almost forgot to mention our small friend [config.example.yaml](https://github.com/PonyLianna/telegram_sticker_bot/blob/dab71970309d0e72a75010ad0951c0972dc1ec22/config.example.yaml).
You need to rename it into `config.yaml`.

_bot->token_ is a thingy you can get from [BotFather](https://t.me/BotFather).

#### Running

You have two options to run it:

`poetry run python telegram_sticker_bot/main.py`
or
`poetry run poe start`

I hope you'll enjoy this small bot <3
