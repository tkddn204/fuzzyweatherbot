#-*- coding: utf-8 -*-
from telegram.ext import Updater

from fuzzyweather.fuzzy.db.fuzzydb import FuzzyDB
from fuzzyweather.util.config import TOKEN, CHANNEL_ID, ALARM_TIME
from fuzzyweather.util.logger import log
from fuzzyweather.handlers.handlers import Handlers
from fuzzyweather.handlers.alarms import Alarms


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
    elif CHANNEL_ID == ('@' or None or ''):
        log.error('!! 채널 아이디를 모르겠어요 !!')
        return

    updater = Updater(token=TOKEN)
    dp = updater.dispatcher
    add_handlers(dp)

    # DB 초기화
    FuzzyDB().__init__()

    # 매일 알람 등록
    if not updater.job_queue.jobs():
        Alarms().daily_alarm_to_channel(CHANNEL_ID, ALARM_TIME.split(" "), updater.job_queue)

    updater.start_polling()
    log.info("fuzzyweatherbot starts polling!")
    updater.idle()
