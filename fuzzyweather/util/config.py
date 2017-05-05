#! /bin/env/python
# Operate config file
import configparser
from fuzzyweather.util.logger import log

config = configparser.ConfigParser()
config.read('setting.ini')

if not config.has_section('credentials'):
    config.add_section('credentials')
    config.set('credentials', 'TOKEN', '')
    # config.set('credentials', 'HOST', '')
    # config.set('credentials', 'PORT', '8443')

if not config.has_section('configs'):
    config.add_section('configs')
    config.set('configs', 'ALARM_TIME', '8')

with open('setting.ini', 'w') as setting:
    config.write(setting)
    setting.close()

TOKEN = config.get('credentials', 'TOKEN')
# HOST = config.get('credentials', 'HOST')
# PORT = config.get('credentials', 'PORT')

ALARM_TIME = 8
try:
    ALARM_TIME = config.getint('configs', 'ALARM_TIME')
except ValueError as e:
    log.warn("알람 타임이 비어있습니다!")
