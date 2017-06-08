from fuzzyweather.fuzzy.fuzzification import Fuzzification
from fuzzyweather.fuzzy.inference_engine import InferenceEngine
from fuzzyweather.fuzzy.defuzzification import Defuzzification
from fuzzyweather.util.logger import log


class FuzzyInference:
    def __init__(self):
        self.found_when = 0
        self.weather_dic = {}
        self.rain_fall_dic = []

    def run(self, when=0):
        # crisp 정보를 받아오고 퍼지화 진행
        fuzzy_set, self.found_when, self.weather_dic, self.rain_fall_dic = \
            Fuzzification().get_fuzzy_set_and_crisp_data(when)

        # 규칙 평가 진행
        res = InferenceEngine().rule_evaluation(fuzzy_set)

        # 규칙 평가를 토대로 역퍼지화 진행
        result_list = Defuzzification().to_crisp_list(res)
        return result_list

    def debug(self, when=0):
        fuzzy_set, self.found_when, self.weather_dic, self.rain_fall_dic = \
            Fuzzification().get_fuzzy_set_and_crisp_data(when)
        debug_fuzzy_set_list = fuzzy_set
        res = InferenceEngine().rule_evaluation(fuzzy_set)
        debug_rule_evaluation_list = res
        result_list = Defuzzification().to_crisp_list(res)
        return result_list, debug_fuzzy_set_list, debug_rule_evaluation_list

    # def test(self, when=0):
    #     fuzzy_set, self.found_when, self.weather_list, self.rain_fall_list = \
    #         Fuzzification().get_fuzzy_set_and_crisp_data(when)
    #     log.error(fuzzy_set)
    #     res = InferenceEngine().rule_evaluation(fuzzy_set)
    #     log.error(res)
    #     result_list = Defuzzification().to_crisp_list(res)
    #     return result_list

# a = FuzzyInference().test(1)
# print(a)
