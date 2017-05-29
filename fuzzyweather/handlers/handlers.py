from telegram.ext import CommandHandler, MessageHandler, Filters, \
                         CallbackQueryHandler

from fuzzyweather.handlers.commands import Commands
from fuzzyweather.handlers.messages import Messages
from fuzzyweather.handlers.inlines import Inlines
from fuzzyweather.util.logger import log


class Handlers(Commands, Messages, Inlines):
    def __init__(self):
        super(Handlers, self).__init__()
        self._handlers = [
            CommandHandler('start', self.command_start),
            CommandHandler('help', self.command_help),
            CommandHandler(['membership', 'ms'], self.command_membership),
            CommandHandler('alarm', self.command_alarm, pass_job_queue=True),
            MessageHandler(Filters.text, self.message_handle),
            CallbackQueryHandler(self.callback_handler)
        ]

    def error_handler(self, bot, update, err):
        log.error('%s : 업데이트 %s 에서 에러 발생 \n %s'
                  % (bot, update, err))

    def get_handlers(self):
        return self._handlers
