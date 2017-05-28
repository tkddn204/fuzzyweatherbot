import os
import re
import emoji

from telegram.chataction import ChatAction
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from fuzzyweather.fuzzy.fuzzy_inference import FuzzyInference
from fuzzyweather.fuzzy.plot import Graph
from fuzzyweather.fuzzy.crisp import Crawling
from fuzzyweather.text import *


class Messages:
    def __init__(self):
        pass

    @staticmethod
    def __weather_message(weather_dic):
        weather_compare_list = {
            '맑음': ':sunny:',
            '구름 조금': ':sunny:',
            '구름 많음': ':partly_sunny:',
            '흐림': ':cloud:',
            '흐리고 비': ':umbrella:'}
        temp_weather = []
        for key, weather in weather_dic.items():
            temp_weather.append(max(weather, key=weather.count))
        max_weather = max(temp_weather, key=temp_weather.count)
        return TEXT_WEATHER.format(weather_compare_list[max_weather], max_weather)

    @staticmethod
    def __rain_fall_message(rain_fall_list):
        for i in range(rain_fall_list.count('-')):
            rain_fall_list.remove('-')
        if len(rain_fall_list) > 0:
            if rain_fall_list[0].find('mm'):
                rain_fall_list[0] = rain_fall_list[0][:-2]
            message = '(강수량 : ' + rain_fall_list[0] + 'mm)'
            return message + TEXT_RAIN_FALL
        else:
            return ''

    @staticmethod
    def __fuzzy_message(result_list):
        time_list = ['오전', '오후', '밤']
        fuzzy_text = TEXT_FUZZY
        for time in time_list:
            if time in result_list:
                fuzzy_text += TEXT_FUZZY_FORMAT.format(
                    result_list[time][2], result_list[time][1],
                    time, result_list[time][0])

        return fuzzy_text

    @staticmethod
    def __fuzzy_debug_message(fuz_list, rul_list):
        msg = ':chart_with_upwards_trend: 퍼지화 결과'
        time_list = ['오전', '오후', '밤']
        for time in time_list:
            if time in fuz_list:
                fuz_item = fuz_list[time]
                msg += '\n[{0}]'.format(time)
                for variable, fuz_value in fuz_item.items():
                    msg += '\n ◇ {0} :'.format(variable)
                    for membership, num in fuz_value.items():
                        if num > 0.0:
                            msg += '\n - {0} : {1:.2f}'.format(membership, num)

        msg += '\n\n :chart_with_downwards_trend: 규칙 평가 결과'
        for time in time_list:
            if time in rul_list:
                rul_item = rul_list[time]
                msg += '\n [{0}]'.format(time)
                for membership, num in rul_item.items():
                    if num > 0.0:
                        msg += '\n - {0} : {1:.2f}'.format(membership, num)

        return msg + '\n'

    def fuzzy_weather_message(self, when=0, debug=''):
        inference_engine = FuzzyInference()

        # fuzzy_text
        fuzzy_text = ''
        if debug is 'debug':
            res_list, fuz_list, rul_list = inference_engine.debug(when)
            fuzzy_text += self.__fuzzy_debug_message(fuz_list, rul_list)
        else:
            res_list = inference_engine.run(when)
        fuzzy_text += self.__fuzzy_message(res_list)

        # fuzzy image
        img_name = Graph().result_file_name(res_list, when)
        path = 'fuzzyweather/fuzzy/result_images/'
        if not os.path.exists(path+img_name):
            Graph().draw_result_list(res_list, img_name, inference_engine.found_when)

        # when_text
        if when is 0:
            if inference_engine.found_when is 0:
                when_text = TEXT_TODAY
            else:
                when_text = TEXT_CAUTION_TOMORROW + TEXT_TOMORROW
            dust = Crawling().get_dust_inf(inference_engine.found_when)
        else:
            dust = Crawling().get_dust_inf(1)
            when_text = TEXT_TOMORROW

        # crisp_text
        crisp_text = self.__weather_message(inference_engine.weather_dic)
        crisp_text += TEXT_DUST.format(dust)
        crisp_text += self.__rain_fall_message(inference_engine.rain_fall_list)

        when_and_crisp_text = emoji.emojize(when_text+crisp_text, use_aliases=True)
        fuzzy_text = emoji.emojize(fuzzy_text, use_aliases=True)
        return when_and_crisp_text, fuzzy_text, img_name

    def message_handle(self, bot, update):
        text = update.message.text
        regex_text = re.compile("오늘|내일").search(text)
        if regex_text:
            regex_text = regex_text.group()
            chat_id = update.message.chat_id
            wait_message = bot.sendMessage(chat_id,
                                           text=TEXT_WAIT)
            bot.send_chat_action(chat_id,
                                 action=ChatAction.TYPING,
                                 timeout=20)

            when = 0 if regex_text in TEXT_WEATHER_LIST[0] else 1
            debug = 'debug' if '디버그' in text else ''
            when_and_crisp_text, fuzzy_text, img_name = \
                self.fuzzy_weather_message(when, debug)

            bot.delete_message(chat_id=chat_id,
                               message_id=wait_message.message_id)
            bot.sendMessage(chat_id=chat_id,
                            text=when_and_crisp_text)
            bot.sendMessage(chat_id=chat_id,
                            text=fuzzy_text,
                            reply_markup=InlineKeyboardMarkup([
                                [InlineKeyboardButton(text=INLINE_GRAPH_SHOW,
                                                      callback_data='show {0}'.format(img_name))]
                            ]))
        else:
            pass
