from fuzzyweather.fuzzy.engine import Inference
from fuzzyweather.fuzzy.crisp import Crawling
from fuzzyweather.text import TEXT_WEATHER_LIST, TEXT_WAIT,\
                              TEXT_TODAY, TEXT_TOMORROW,\
                              TEXT_FUZZY, TEXT_FUZZY_FORMAT


class Messages:
    def __init__(self):
        pass

    @staticmethod
    def __fuzzy_message(res_list):
        fuzzy_text = TEXT_FUZZY
        for d in reversed(list(res_list.keys())):
            fuzzy_text += TEXT_FUZZY_FORMAT.format(
                res_list[d][2], d, res_list[d][1])
        return fuzzy_text

    def message_handle(self, bot, update):
        text = update.message.text

        if text in TEXT_WEATHER_LIST:
            chat_id = update.message.chat_id
            bot.sendMessage(chat_id,
                            text=TEXT_WAIT)
            if text in TEXT_WEATHER_LIST[0]:
                day = 0
                dust = Crawling().get_dust_inf()
                fuzzy_text = TEXT_TODAY.format(dust)
            else:
                day = 1
                fuzzy_text = TEXT_TOMORROW
            res_list = Inference().run(day)
            fuzzy_text += self.__fuzzy_message(res_list)
            bot.sendMessage(update.message.chat_id,
                            text=fuzzy_text)
        else:
            pass
