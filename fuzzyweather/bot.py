#-*- coding: utf-8 -*-
from telegram.ext import Updater

from fuzzyweather.fuzzy.db.fuzzydb import FuzzyDB
from fuzzyweather.util.config import TOKEN
from fuzzyweather.util.logger import log
from fuzzyweather.handlers.handlers import Handlers


def add_handlers(dp):
    handlers = Handlers()
    for handler in handlers.get_handlers():
        dp.add_handler(handler)
    dp.add_error_handler(handlers.error_handler)


def main():
    log.info("fuzzyweatherbot is setting...")
    if TOKEN == '':
        log.error('!! 토큰이 없어요 !!')
        return

    updater = Updater(token=TOKEN)
    dp = updater.dispatcher
    add_handlers(dp)

    # 매일 아침 8시 알람 등록
    # if not updater.job_queue.jobs():
    #     updater.job_queue.run_daily()

    # DB 초기화
    FuzzyDB().__init__()

    updater.start_polling()
    log.info("fuzzyweatherbot starts polling!")
    updater.idle()
