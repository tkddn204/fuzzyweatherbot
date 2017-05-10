import requests
from bs4 import BeautifulSoup

KMA_URL = 'http://www.kma.go.kr/weather/forecast/timeseries.jsp?searchType=INTEREST&wideCode=%s&cityCode=%s&dongCode=%s'
WIDE_CODE = '3000000000'
CITY_CODE = '3020000000'
DONG_CODE = '3020053000'


def clean_data(data=(), today=0, tomorrow=0):
    if tomorrow > 1:
        return [i[today:today+tomorrow] for i in data]
    else:
        return [i[:today] for i in data]


# day = 0 -> 오늘, day = 1 -> 내일
def get_weather_inf(url, day=0):
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    table = soup.find('table', attrs={'class': 'forecastNew3'})
    data = []

    # 테이블 안의 내용 가져오기
    rows = table.find('tbody').find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])

    # 테이블 정리
    for weather in table.find_all('td', attrs={'class': 'PD_none'}):
        data[2].append(weather.get('title')) # 날씨 추가
    data.remove([])
    avg_temperature = data.pop(4)

    # 강수량 교체
    rainfall = []
    for i, row in enumerate(data.pop(3)):
        rainfall.append(row)
        if i > 1:
            rainfall.append(row)
    data.insert(3, rainfall)

    # 오늘과 내일 칼럼 수
    today = 0
    tomorrow = 0
    if table.find('th', attrs={'class': 'today'}):
        today = int(table.find('th', attrs={'class': 'today'}).get('colspan'))
    if day is 1:
        tomorrow = int(table.find('th', attrs={'class': 'tommorow'}).get('colspan'))

    # 최종 데이터 내보내기
    weather_table = clean_data(data, today, tomorrow)
    return weather_table, avg_temperature[day]

# 사용방법
# 오늘 날씨는 맨 뒤 없어도됨, 내일 날씨는 맨 뒤에 1
# data, avg_temperature = get_weather_inf(KMA_URL % (WIDE_CODE, CITY_CODE, DONG_CODE), 1)
# for d in data:
#    print(d)
