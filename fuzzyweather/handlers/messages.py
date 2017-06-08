import os
import re
import emoji

from telegram.chataction import ChatAction
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from fuzzyweather.fuzzy.fuzzy_main import FuzzyInference
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
            for weather_item in weather:
                temp_weather.append(weather_item)
        max_weather = max(temp_weather, key=temp_weather.count)
        if max_weather in weather_compare_list:
            return TEXT_WEATHER.format(weather_compare_list[max_weather], max_weather)
        else:
            return TEXT_WEATHER.format(weather_compare_list['흐리고 비'], max_weather)

    @staticmethod
    def __rain_fall_message(rain_fall_dic):
        time_list = ['밤', '오후', '오전']
        rain_fall_mm_msg = ''
        time_msg = ''
        for index, rain in rain_fall_dic.items():
            for i in range(rain.count('-')):
                rain.remove('-')
            if len(rain) > 0:
                if len(rain) > 1:
                    temp_index = 0
                    for i, rain_item in enumerate(rain):
                        if int(rain_item[0]) > temp_index:
                            temp_index = i
                    rain[0] = rain[temp_index]
                if rain[0].find('mm') is not -1:
                    rain[0] = rain[0][:-2]
                rain_fall_mm_msg = rain[0]
                time_msg += time_list[index] + ', '
            else:
                if rain_fall_mm_msg is '' and index is len(rain_fall_dic)-1:
                    return ''
                else:
                    continue

        return TEXT_RAIN_FALL.format(time_msg[:-2], rain_fall_mm_msg)

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
        crisp_text += self.__rain_fall_message(inference_engine.rain_fall_dic)

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
            debug = 'debug' if '자세히' in text else ''
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
