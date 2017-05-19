import requests
from bs4 import BeautifulSoup


class Crawling:
    def __init__(self, **where):
        self.__KMA_URL = 'http://www.kma.go.kr/weather/forecast/timeseries.jsp?searchType=INTEREST&wideCode=%s&cityCode=%s&dongCode=%s'
        self.__DUST_URL = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80'
        if where:
            self.__WIDE_CODE = where['WIDE_CODE']
            self.__CITY_CODE = where['CITY_CODE']
            self.__DONG_CODE = where['DONG_CODE']
            self.__AREA_CODE = where['AREA_CODE']
        else:
            self.__WIDE_CODE = '3000000000'
            self.__CITY_CODE = '3020000000'
            self.__DONG_CODE = '3020053000'
        self._URL = self.__KMA_URL % (
            self.__WIDE_CODE, self.__CITY_CODE, self.__DONG_CODE)

    @staticmethod
    def __clean_up_data(data=(), today=0, tomorrow=0):
        if tomorrow > 1:
            return [i[today:today+tomorrow] for i in data]
        else:
            return [i[:today] for i in data]

    # day = 0 -> 오늘, day = 1 -> 내일
    def get_weather_inf(self, day=0):
        # 기상청
        soup = BeautifulSoup(requests.get(self._URL).text, 'html.parser')
        table = soup.find('table', attrs={'class': 'forecastNew3'})
        # 미세먼지
        dust_soup = BeautifulSoup(requests.get(self.__DUST_URL).text, 'html.parser')
        dust_table = dust_soup.find('div', attrs={'class': 'tb_scroll'})
        data = []

        # 테이블 안의 내용 가져오기
        rows = table.find('tbody').find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        # 미세먼지 가져오기
        rows = dust_table.find('tbody').find_all('tr')
        dust = ''
        for row in rows:
            if row.find('th').text in '대전':
                dust = row.find_all('td')[1].text

        # 테이블에 날씨 정보 추가 및 빈 리스트 정리
        for weather in table.find_all('td', attrs={'class': 'PD_none'}):
            data[2].append(weather.get('title'))  # 날씨 추가
        data.remove([])
        # 최저/최고 온도 pop
        data.pop(4)

        # 강수량 정리(1개 정보를 2개씩 보이도록
        rainfall = []
        for i, row in enumerate(data.pop(3)):
            rainfall.append(row)
            if i > 0:
                rainfall.append(row)
        data.insert(3, rainfall)

        # 오늘과 내일의 칼럼 수 리턴
        today = 0
        tomorrow = 0
        if table.find('th', attrs={'class': 'today'}):
            today = int(table.find('th', attrs={'class': 'today'}).get('colspan'))

        # 오늘 저녁 9시 이후는 내일 날짜로 출력
        if today <= 1:
            day = 1

        if day is 1:
            tomorrow = int(table.find('th', attrs={'class': 'tommorow'}).get('colspan'))

        # 최종 데이터 내보내기
        weather_table = self.__clean_up_data(data, today, tomorrow)
        return weather_table, dust

# 사용방법
# 오늘 날씨는 no parameter, 내일 날씨는 1
dat, dus = Crawling().get_weather_inf()
for d in dat:
    print(d)
print(dus)
