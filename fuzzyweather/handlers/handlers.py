from telegram.ext import CommandHandler, MessageHandler, Filters

from fuzzyweather.handlers.commands import Commands
from fuzzyweather.handlers.messages import Messages
from fuzzyweather.util.logger import log


class Handlers(Commands, Messages):
    def __init__(self):
        super(Handlers, self).__init__()
        self._handlers = [
            CommandHandler('start', self.command_start),
            CommandHandler('help', self.command_help),
            CommandHandler(['membership', 'ms'], self.command_membership),
            MessageHandler(Filters.text, self.message_handle),
        ]

    def error_handler(self, bot, update, err):
        log.error('%s : 업데이트 %s 에서 에러 발생 \n %s'
                  % (bot, update, err))

    def get_handlers(self):
        return self._handlers
