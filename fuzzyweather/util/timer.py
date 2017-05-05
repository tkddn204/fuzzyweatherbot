# 텍스트를 받아와서 시간으로 바꾸는 곳.. 파일명이 딱히 생각이 안나서 timer로 함
import re
import datetime
from string import Template

from HBhelper.text import ALARM_TIME_TEMPLATE, TEXT_TIME_DIVIDE


class DeltaTemplate(Template):
    delimiter = "%"


def now_date():
    return datetime.datetime.now().date()


def now_time():
    t = datetime.datetime.now()
    rt = t - datetime.timedelta(seconds=t.second,
                                microseconds=t.microsecond)
    return rt.time()


def alarm_time_combine(date, time):
    return datetime.datetime.combine(date, time)


def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    d["H"], rem = divmod(tdelta.seconds, 3600)
    d["M"], d["S"] = divmod(rem, 60)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)


def str_alarm_time(time):
    tdelta = time - datetime.datetime.now()
    strt = strfdelta(tdelta, ALARM_TIME_TEMPLATE)
    return_time = strt.split(' ')
    view_time = ''
    for count in range(4):
        if return_time[count] is not '0':
            view_time += (return_time[count] + TEXT_TIME_DIVIDE[count] + ' ')
    return view_time


def str_repeat_alarm_time(time):
    if isinstance(time, datetime.time):
        t = [str(time.hour), str(time.minute)]
    elif isinstance(time, datetime.datetime):
        t = [str(time.hour), str(time.minute)]
    else:
        t = time.split(":")
    view_time = ''
    for count in range(2):
        view_time += (t[count] + TEXT_TIME_DIVIDE[count+1] + ' ')
    return view_time


def to_datetime(str_time):
    if len(str_time) < 17:
        # return datetime.time()
        return datetime.datetime.strptime(str_time, "%H:%M:%S").time()
    else:
        return datetime.datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S.%f")


def alarm_set_days(text):
    '''일(0)~토(6), 매일(7)
       숫자형 문자열로 반환된다.
    '''
    r = re.compile('[\d]')
    conversion = r.findall(text)
    try:
        if conversion:
            if not (conversion.count('7')
                    or conversion.count('8')
                    or conversion.count('9')):
                l = list(set(conversion))
                l.sort()
                return l

        return '7'
    except Exception:
        return '7'


def alarm_set_dates(text):
    ''' 2017년 2월 24일
        return : datetime.date
    '''
    r = re.compile('[\d]+')
    con = r.findall(text)
    date = now_date()
    # 3개 파라메터
    try:
        if con:
            # 년(0) 월(1) 일(2)
            if len(con) == 3:
                year = int(con[0])
                month = int(con[1])
                day = int(con[2])
                year = year if year < 100 else year + 2000
                if date.year <= year or year <= 9999:
                    if month >= 0 or month <= 12:
                        if day >= 0 or day <= 31:
                            return datetime.date(year, month, day)
                else:
                    if month >= 0 or month <= 12:
                        if day >= 0 or day <= 31:
                            return datetime.date(date.year, month, day)
                    else:
                        if day >= 0 or day <= 31:
                            return datetime.date(date.year, date.month, day)

            # 월(0) 일(1)
            elif len(con) == 2:
                month = int(con[0])
                day = int(con[1])
                if (date.month <= month) and (month >= 0 or month <= 12):
                    if day >= 0 or day <= 31:
                        return datetime.date(date.year, month, day)

            # 일(0)
            elif len(con) == 1:
                day = int(con[0])
                if day >= 0 or day <= 31:
                    if date.day <= day:
                            return datetime.date(date.year, date.month, day)
                    else:
                        return datetime.date(date.year, date.month+1, day)

        return date
    except Exception:
        return date


def alarm_set_time(text):
    r = re.compile('[\d]+')
    con = r.findall(text)
    time = now_time()
    try:
        if con:
            # 시(0) 분(1)
            if len(con) == 2:
                hour = int(con[0])
                minute = int(con[1])
                if hour >= 0 or hour <= 23:
                    if minute >= 0 or minute <= 24:
                        return datetime.time(hour, minute)

            # 시(1)
            elif len(con) == 1:
                hour = int(con[0])
                if hour >= 0 or hour <= 24:
                    return datetime.time(hour)

        return time
    except Exception:
        return time
