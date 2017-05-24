from fuzzyweather.fuzzy.membership import Membership
from fuzzyweather.fuzzy.crisp import Crawling

AM_LIST = ['03', '06', '09']
PM_LIST = ['12', '15']
NT_LIST = ['18', '21', '24']


class Fuzzification(Membership):
    def __init__(self, when=0):
        super(Fuzzification, self).__init__()
        self.__morning = []
        self.__afternoon = []
        self.__night = []

        # crisp 데이터에서 기온과 습도만 가져옴
        self.__crisp_data, self.__day = self.__choose_data(when)

        # 밤, 오후, 오전으로 나눔(각 평균 출력, 강수량 출력 - 날짜 제외)
        self.__day_list, self.rain_fall = self.__split_day()

        # 멤버쉽 함수에 따라 매핑
        self.__fuzzyset_with_crisp = self._set_before_membership(self.__day_list)

    @staticmethod
    def __choose_data(day):
        # crisp 데이터와 데이터의 날짜를 받아옴
        crisp_data, d = Crawling().get_weather_inf(day)
        print(crisp_data)
        return crisp_data, d

    def __split_time(self):
        bool_list = []
        for li in [AM_LIST, PM_LIST, NT_LIST]:
            num = [a in li for a in self.__crisp_data[0]].count(True)
            bool_list.append(num)
        return bool_list

    def __split_day(self):
        cut_time = self.__split_time()
        day_list = [[], [], []]
        # avg_list = [[0, [], 0, 0, 0, 0] for i in range(3)]
        avg_list = [[0., 0., 0.] for i in range(3)]
        rain_fall = []
        for i, n in enumerate(reversed(cut_time)):
            # 밤, 오후, 오전을 나눔
            if n == 0:
                continue
            for k in range(n):
                day_list[i].append([col.pop() for col in self.__crisp_data])
            # 각 평균을 구함(날짜, 풍속 제외)
            # 강수량은 리스트 그대로(따로 뺌)
            for m, row in enumerate([3]):
                rain_fall = [day_list[i][k][row] for k in range(n)]
            # 기온, 습도, 강수확률(구름량)
            for m, row in enumerate([4, 6, 2]):
                avg_list[i][m] = float(sum(int(day_list[i][k][row]) for k in range(n))/n)
        return avg_list, rain_fall

    def get_fuzzyset_and_day(self):
        return self.__fuzzyset_with_crisp, self.__day

# f = Fuzzification()
# fs, d = f.get_fuzzyset_and_day()
# print(fs, d)
