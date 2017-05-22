from fuzzyweather.fuzzy.engine import Inference
from fuzzyweather.fuzzy.crisp import Crawling


class Messages:
    def __init__(self):
        pass

    @staticmethod
    def __fuzzy_message(res_list):
        fuzzy_text = '퍼지 분석 결과: \n'
        for d in reversed(list(res_list.keys())):
            fuzzy_text += '[{0:.1f}] {1}에는 {2}\n'.format(
                res_list[d][2], d, res_list[d][1])
        return fuzzy_text

    def message_handle(self, bot, update):
        text = update.message.text

        if text in ['오늘의 날씨', '내일의 날씨']:
            bot.sendMessage(update.message.chat_id,
                            text='잠시만 기다려주세요...')
            if text in '오늘의 날씨':
                res_list = Inference().start()
                dust = Crawling().get_dust_inf()
                bot.sendMessage(update.message.chat_id,
                                text='한밭대 오늘의 날씨 \n'
                                     '미세먼지 : ' + dust)
                fuzzy_text = self.__fuzzy_message(res_list)
            else:
                res_list = Inference().start(1)
                bot.sendMessage(update.message.chat_id,
                                text='한밭대 내일의 날씨 \n')
                fuzzy_text = self.__fuzzy_message(res_list)
            bot.sendMessage(update.message.chat_id,
                            text=fuzzy_text)
        else:
            pass
