# Telegram_Sticker_Bot

Simple Telegram bot for stickers debugging written on [python-telegram-bot](https://python-telegram-bot.org/)

### What it can do? 
Well... It can send you *UniqueID*, or *ID* of Sticker and StickerPack, that can help you on debugging your own sticker pack. 

Right now it can also download and show you all of them in *DocumentList* or *ImageList*. 

Either it *webp* (plain stickers) or *webm* (animated stickers) it can group and give you a plain look on those to debug or just download.

### How to install?

Pretty simple!
`git clone https://github.com/PonyLianna/telegram_sticker_bot`

Then in the folder:
`pip install poetry`
`poetry install`

It will install all necessary requirements and you're ready to start!

#### Dealing with config
Almost forgot to mention our small friend `config.example.yaml`. 
You need to rename it into `config.yaml`. 
*bot->token* is a thingy you can get from [BotFather](@BotFather).

#### Running 

You have two options to run it: 
`poetry run python telegram_sticker_bot/main.py`
or
`poetry run poe start`

I hope you'll enjoy this small bot <3