from datetime import datetime, date, time

Y = 2000 # dummy leap year to allow input X-02-29 (leap day)
seasons = [('겨울', (date(Y,  1,  1),  date(Y,  3, 20))),
           ('봄', (date(Y,  3, 21),  date(Y,  6, 20))),
           ('여름', (date(Y,  6, 21),  date(Y,  9, 22))),
           ('가을', (date(Y,  9, 23),  date(Y, 12, 20))),
           ('겨울', (date(Y, 12, 21),  date(Y, 12, 31)))]


def get_season(now=date.today()):
    if isinstance(now, datetime):
        now = now.date()
    now = now.replace(year=Y)
    return next(season for season, (start, end) in seasons
                if start <= now <= end)


def get_hour_time(when='8'):
    return time(hour=int(when))
