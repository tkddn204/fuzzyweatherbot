from fuzzyweather.fuzzy.fuzzy_inference import FuzzyInference
from fuzzyweather.fuzzy.crisp import Crawling
from fuzzyweather.text import *
from telegram.chataction import ChatAction
import emoji


class Messages:
    def __init__(self):
        pass

    @staticmethod
    def __weather_message(weather_list):
        weather_compare_list = {
            '맑음': ':sunny:',
            '구름 조금': ':sunny:',
            '구름 많음': ':partly_sunny:',
            '흐림': ':cloud:',
            '흐리고 비': ':umbrella:'}
        return emoji.emojize(TEXT_WEATHER.format(
            weather_compare_list[weather_list[0]], weather_list[0]), use_aliases=True)

    @staticmethod
    def __rain_fall_message(rain_fall_list):
        for i in range(rain_fall_list.count('-')):
            rain_fall_list.remove('-')
        if len(rain_fall_list) > 0:
            msg = TEXT_RAIN_FALL
            if not rain_fall_list[0].find('mm'):
                rain_fall_list[0] += 'mm'
            msg += '(' + rain_fall_list[0] + ')\n'
            return msg
        else:
            return ''

    @staticmethod
    def __fuzzy_message(res_list):
        time_list = ['오전', '오후', '밤']
        fuzzy_text = TEXT_FUZZY
        for time in time_list:
            if time in res_list:
                fuzzy_text += TEXT_FUZZY_FORMAT.format(
                    res_list[time][2], res_list[time][1], time, res_list[time][0])
        return fuzzy_text

    def message_handle(self, bot, update):
        text = update.message.text

        if text in TEXT_WEATHER_LIST:
            chat_id = update.message.chat_id
            msg = bot.sendMessage(chat_id,
                                  text=TEXT_WAIT)
            bot.send_chat_action(chat_id,
                               action=ChatAction.TYPING,
                               timeout=30)

            inference_engine = FuzzyInference()
            when = 0 if text in TEXT_WEATHER_LIST[0] else 1
            res_list = inference_engine.run(when)

            crisp_text = ''
            # when_text
            if when is 0:
                if inference_engine.found_when is 0:
                    when_text = TEXT_TODAY
                    crisp_text = self.__weather_message(inference_engine.weather_list)
                else:
                    when_text = TEXT_CAUTION_TOMORROW + TEXT_TOMORROW
                dust = Crawling().get_dust_inf(inference_engine.found_when)
            else:
                dust = Crawling().get_dust_inf(1)
                when_text = TEXT_TOMORROW

            # crisp_text
            crisp_text += TEXT_DUST.format(dust)
            crisp_text += self.__rain_fall_message(inference_engine.rain_fall_list)

            # fuzzy_text
            fuzzy_text = self.__fuzzy_message(res_list)

            bot.delete_message(chat_id=chat_id,
                               message_id=msg.message_id)
            bot.sendMessage(chat_id=chat_id,
                            text=when_text+crisp_text)
            bot.sendMessage(chat_id=chat_id,
                            text=emoji.emojize(fuzzy_text, use_aliases=True))
        else:
            pass
