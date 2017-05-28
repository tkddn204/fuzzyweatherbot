from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from fuzzyweather.text import INLINE_GRAPH_SHOW, TEXT_WAIT, \
                                INLINE_GRAPH_HIDE


class Inlines:
    def __init__(self):
        pass

    def __hide_result_graph(self, bot, query, data):
        chat_id = query.from_user.id
        delete_message_id = data[1]
        img_name = data[2]

        bot.delete_message(chat_id, delete_message_id)
        query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([
                                            [InlineKeyboardButton(
                                                text=INLINE_GRAPH_SHOW,
                                                callback_data='show {0}'.format(img_name))]
                                        ]))

    def __show_result_graph(self, bot, query, data):
        chat_id = query.from_user.id
        img_name = data[1]

        # 잠시만 기다려주세요...
        query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([
                                            [InlineKeyboardButton(
                                                text=TEXT_WAIT,
                                                callback_data=' '
                                            )]
                                        ]))

        path = 'fuzzyweather/fuzzy/result_images/'
        msg = bot.send_photo(chat_id, open(path+img_name, 'rb'))
        query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([
                                            [InlineKeyboardButton(
                                                text=INLINE_GRAPH_HIDE,
                                                callback_data='hide {0} {1}'.format(msg.message_id, img_name))]
                                        ]))

    def callback_handler(self, bot, update):
        query = update.callback_query
        data = query.data.split(' ')

        if len(data) > 0:
            if 'show' in data:
                self.__show_result_graph(bot, query, data)
            elif 'hide' in data:
                self.__hide_result_graph(bot, query, data)
            else:
                pass
            return
        else:
            pass
