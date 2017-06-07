from fuzzyweather.handlers.alarms import Alarms
from fuzzyweather.text import TEXT_START, TEXT_HELP, KEYBOARD_SELECT,\
                              TEXT_MEMBERSHIP, TEXT_BEFORE_MEMBERSHIP,\
                              TEXT_AFTER_MEMBERSHIP
from telegram import ReplyKeyboardMarkup


class Commands:
    def __init__(self):
        pass

    def command_start(self, bot, update):
        user_name = update.message.from_user.first_name

        bot.sendMessage(
            update.message.chat_id,
            text=TEXT_START.format(
                user_name=user_name, bot_name=bot.name),
            reply_markup=ReplyKeyboardMarkup(KEYBOARD_SELECT))
        bot.sendMessage(
            update.message.chat_id,
            text=TEXT_HELP)

    def command_help(self, bot, update):
        bot.sendMessage(
            update.message.chat_id,
            text=TEXT_HELP)

    def command_membership(self, bot, update):
        bot.sendMessage(
            update.message.chat_id,
            text=TEXT_MEMBERSHIP)
        bot.send_photo(
            update.message.chat_id,
            open('fuzzyweather/fuzzy/membership_images/before_membership.png', 'rb'),
            caption=TEXT_BEFORE_MEMBERSHIP)
        bot.send_photo(
            update.message.chat_id,
            open('fuzzyweather/fuzzy/membership_images/after_membership.png', 'rb'),
            caption=TEXT_AFTER_MEMBERSHIP)

    def command_alarm(self, bot, update, job_queue):
        if '@SsangWoo' in update.message.from_user.name:
            Alarms().alarm_update(bot, job_queue)
