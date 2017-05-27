from fuzzyweather.util.timer import get_hour_time
from fuzzyweather.handlers.messages import Messages


class Alarms:
    def __init__(self):
        pass

    def alarm_update(self, bot, job):
        context_list = job if isinstance(job, str) else job.context
        channel_id, when = context_list.split(" ")
        when = 1 if int(when) >= 18 else 0

        when_and_crisp_text, fuzzy_text = \
            Messages().fuzzy_weather_message(when)

        bot.sendMessage(channel_id,
                        text='{0} {1}'.format(when_and_crisp_text, fuzzy_text))

    def daily_alarm_to_channel(self, channel_id, when_list, job_queue):
            for when in when_list:
                job_context = '{0} {1}'.format(channel_id, when)
                job_queue.run_daily(self.alarm_update,
                                    time=get_hour_time(when),
                                    context=job_context,
                                    name=job_context)
