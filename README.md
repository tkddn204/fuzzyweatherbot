
# FuzzyWeatherbot

퍼지 로직으로 **한밭대학교**(정확히 대전광역시 유성구 온천1동)의 날씨를 알려주는 텔레그램 봇입니다. 한국어 전용입니다.(Only korean)
봇으로 매일 8시, 20시에 날씨 알림을 해주는 채널도 있습니다.

본 프로그램은 **절대** 상업용 목적을 가지고 있지 않으며, 그저 학교 프로젝트일 뿐입니다...

* Bot link : **[@fuzzyweatherbot](http://telegram.me/fuzzyweatherbot)**
* Channel link : **[@hanbatweather](https://t.me/hanbatweather)**

## 날씨 정보

날씨는 [`BeautifulSoap4`](https://www.crummy.com/software/BeautifulSoup/)와 [`requests`](http://docs.python-requests.org/en/master/)를 이용해 다음 사이트를 웹 크롤링(웹 스크래핑)했습니다.

* [기상청 동네예보](http://www.kma.go.kr/weather/forecast/timeseries.jsp?searchType=INTEREST&wideCode=3000000000&cityCode=3020000000&dongCode=3020053000)
* [에어코리아 대기질 예보](http://www.airkorea.or.kr/dustForecast)

※ 혹시 법적으로 문제가 생기게 되면 꼭 연락 부탁드립니다!(법 관련 부분은 잘 모르기 때문입니다)

## TODO

* 전국 검색 기능
* 전국 날씨 예보

## 학생~~개발자~~ 정보

* 텔레그램 : [@SsangWoo](https://t.me/SsangWoo)
* 이메일 : tkddn204@gmail.com