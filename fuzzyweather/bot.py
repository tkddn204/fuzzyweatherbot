#-*- coding: utf-8 -*-
from telegram.ext import Updater

from fuzzyweather.util.config import TOKEN
from fuzzyweather.util.logger import log
from fuzzyweather.handlers.handlers import Handlers


def add_handlers(dp):
    handlers = Handlers()
    for handler in handlers.get_handlers():
        dp.add_handler(handler)
    dp.add_error_handler(handlers.error_handler)


def main():
    log.info("Bot is setting...")
    if TOKEN == '':
        log.error('!! 토큰이 없어요 !!')
        return

    updater = Updater(token=TOKEN)
    dp = updater.dispatcher
    add_handlers(dp)

    updater.start_polling()
    log.info("Bot starts polling!")
    updater.idle()
