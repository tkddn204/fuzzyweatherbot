import re
import requests
from bs4 import BeautifulSoup

KMA_URL = 'http://www.kma.go.kr/weather/forecast/timeseries.jsp?searchType=INTEREST&wideCode=%s&cityCode=%s&dongCode=%s'
WIDE_CODE = '3000000000'
CITY_CODE = '3020000000'
DONG_CODE = '3020053000'


def get_weather_inf(url):
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    table = soup.find('table', attrs={'class': 'forecastNew3'})
    data = []

    rows = table.find('tbody').find_all('tr')
    # 테이블 안의 내용 가져오기
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    # 테이블 정리
    for weather in table.find_all('td', attrs={'class': 'PD_none'}):
        data[2].append(weather.get('title')) # 날씨 추가
    data.remove(data[0])
    data.remove(data[3])

    # 강수량 교체
    col = []
    content = []
    for row in table.find_all('td', colspan=re.compile('[1-2]')):
        col.append(row.get('colspan'))
        content.append(row.contents[0].strip())
    rainfall = col, content
    data.insert(3, rainfall)

    #오늘과 내일 col
    today = table.find('th', attrs={'class': 'today'}).get('colspan')
    tomorrow = table.find('th', attrs={'class': 'tommorow'}).get('colspan')
    data.append((today, tomorrow))

    return data

# 사용방법
# get_weather_inf(KMA_URL % (WIDE_CODE, CITY_CODE, DONG_CODE))
