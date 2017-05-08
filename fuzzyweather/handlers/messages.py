

class Messages:
    def __init__(self):
        pass

    def message_handle(self, bot, update):
        text = update.message.text

        if text in '오늘의 날씨':
            bot.sendMessage(update.message.chat_id,
                            text='한밭대 오늘의 날씨 \n'
                                 '구름 조금 \n'
                                 '평균 온도 : 20℃ \n'
                                 '평균 습도 : 30%')
            bot.sendMessage(update.message.chat_id,
                            text='봇의 한마디: \n'
                                 '오늘은 날씨가 좋네요! \n'
                                 '밖에 나가서 나들이라도 하는 게 어떨까요?')
        elif text in '내일의 날씨':
            bot.sendMessage(update.message.chat_id,
                            text='한밭대 내일의 날씨 \n'
                                 '강한 비 \n'
                                 '평균 온도 : 10℃ \n'
                                 '평균 습도 : 80% \n'
                                 '강수 확률 : 80%')
            bot.sendMessage(update.message.chat_id,
                            text='봇의 한마디: \n'
                                 '밖이 쌀쌀해요! 옷을 챙겨 입으세요!\n'
                                 '밖에 나갈 땐 우산을 가져가세요!')
        else:
            pass
