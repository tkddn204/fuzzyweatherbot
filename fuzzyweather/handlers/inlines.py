from telegram import InlineKeyboardMarkup, InlineKeyboardButton, \
    InlineQueryResultArticle, InputTextMessageContent, ParseMode

from fuzzyweather.text import INLINE_GRAPH_SHOW, TEXT_WAIT, \
                                INLINE_GRAPH_HIDE


class Inlines:
    def __init__(self):
        pass

    def __hide_result_graph(self, bot, query, delete_message_id):
        chat_id = query.from_user.id

        bot.delete_message(chat_id, delete_message_id)
        query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([
                                            [InlineKeyboardButton(
                                                text=INLINE_GRAPH_SHOW,
                                                callback_data='show')]
                                        ]))

    def __show_result_graph(self, bot, query):
        chat_id = query.from_user.id

        # 잠시만 기다려주세요...
        query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([
                                            [InlineKeyboardButton(
                                                text=TEXT_WAIT,
                                                callback_data=' '
                                            )]
                                        ]))
        # TODO 그래프가 없으면 생성, 있으면 캐싱
        msg = bot.send_photo(chat_id,
                             open('fuzzyweather/fuzzy/membership_images/before_membership.png', 'rb'))
        query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([
                                            [InlineKeyboardButton(
                                                text=INLINE_GRAPH_HIDE,
                                                callback_data='hide {0}'.format(msg.message_id))]
                                        ]))

    def callback_handler(self, bot, update):
        query = update.callback_query
        data = query.data.split(' ')

        if len(data) > 0:
            if 'show' in data:
                self.__show_result_graph(bot, query)
            elif 'hide' in data:
                self.__hide_result_graph(bot, query, data[1])
            else:
                pass
            return
        else:
            pass
