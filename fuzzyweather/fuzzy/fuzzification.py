from fuzzyweather.fuzzy.membership import Membership
from fuzzyweather.fuzzy.crisp import Crawling


class Fuzzification(Membership):
    def __init__(self):
        super(Fuzzification, self).__init__()
        self.__morning = []
        self.__afternoon = []
        self.__night = []

    @staticmethod
    def __get_crisp_data(when):
        # crisp 데이터와 데이터의 날짜(오늘:0, 내일:1)를 받아옴
        crisp_data, day = Crawling().get_weather_inf(when)
        return crisp_data, day

    @staticmethod
    def __split_time(crisp_data):
        am_list = ['03', '06', '09']
        pm_list = ['12', '15']
        nt_list = ['18', '21', '24']
        split_border_list = []
        table_time = crisp_data[0]
        for list_element in [am_list, pm_list, nt_list]:
            num = [time_col in list_element for time_col in table_time].count(True)
            split_border_list.append(num)
        return split_border_list

    def __split_table_according_to_time(self, crisp_data):
        split_time_list = self.__split_time(crisp_data)
        time_list = [[], [], []]
        # avg_list = [[0, [], 0, 0, 0, 0] for i in range(3)]
        avg_time_list = [[0., 0., 0.], [0., 0., 0.], [0., 0., 0.]]
        weather_dic = {}
        rain_fall_dic = {}

        for index, split_time in enumerate(reversed(split_time_list)):
            # 밤, 오후, 오전을 나눔
            if split_time is 0:
                continue
            for n in range(split_time):
                time_list[index].append([col.pop() for col in crisp_data])

            # 날씨와 강수량은 따로 리스트 만들어서 뺌
            weather_dic[index] = [time_list[index][col][1] for col in range(split_time)]
            rain_fall_dic[index] = [time_list[index][col][3] for col in range(split_time)]

            # 각 평균을 구함(강수확률(구름량), 기온, 습도)
            for m, row in enumerate([2, 4, 6]):
                avg_time_list[index][m] = float(sum(int(time_list[index][k][row])
                                                    for k in range(split_time)) / split_time)
        return avg_time_list, weather_dic, rain_fall_dic

    def get_fuzzy_set_and_crisp_data(self, when=0):
        # crisp 데이터와 날짜 정보를 얻어옴
        crisp_data, time = self.__get_crisp_data(when)

        # 밤, 오후, 오전으로 나눔(각 평균 출력, 강수량 출력 - 날짜 제외)
        split_time_list, weather_dic, rain_fall_dic = self.__split_table_according_to_time(crisp_data)

        # 멤버쉽 함수에 따라 매핑
        crisp_to_fuzzy_set = self._set_crisp_membership(split_time_list)
        return crisp_to_fuzzy_set, time, weather_dic, rain_fall_dic

# f = Fuzzification()
# fs, d, r = f.get_fuzzy_set_and_crisp_data()
# print(fs, d, r)
