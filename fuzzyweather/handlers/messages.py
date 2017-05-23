from fuzzyweather.fuzzy.engine import Inference
from fuzzyweather.fuzzy.crisp import Crawling
from fuzzyweather.text import TEXT_WEATHER_LIST, TEXT_WAIT,\
                              TEXT_TODAY, TEXT_TOMORROW,\
                              TEXT_FUZZY, TEXT_FUZZY_FORMAT,\
                              TEXT_CAUTION_TOMORROW
from telegram.chataction import ChatAction
import emoji


class Messages:
    def __init__(self):
        pass

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

            inference = Inference()
            when = 0 if text in TEXT_WEATHER_LIST[0] else 1
            res_list = inference.run(when)
            if when is 0:
                if inference.day is 0:
                    dust = Crawling().get_dust_inf()
                    fuzzy_text = TEXT_TODAY.format(dust)
                else:
                    fuzzy_text = TEXT_CAUTION_TOMORROW + TEXT_TOMORROW
            else:
                fuzzy_text = TEXT_TOMORROW
            fuzzy_text += self.__fuzzy_message(res_list)
            bot.delete_message(chat_id=chat_id,
                               message_id=msg.message_id)
            bot.sendMessage(chat_id=chat_id,
                            text=emoji.emojize(fuzzy_text, use_aliases=True))
        else:
            pass
