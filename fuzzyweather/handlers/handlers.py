from telegram.ext import CommandHandler

from fuzzyweather.handlers.commands import Commands
from fuzzyweather.util.logger import log


class Handlers(Commands):
    def __init__(self):
        super(Handlers, self).__init__()
        self._handlers = [
            CommandHandler('start', self.command_start),
            CommandHandler('help', self.command_help),
        ]

    def error_handler(self, bot, update, err):
        log.error('%s : 업데이트 %s 에서 에러 발생 \n %s'
                  % (bot, update, err))

    def get_handlers(self):
        return self._handlers
