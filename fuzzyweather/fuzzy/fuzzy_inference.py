from fuzzyweather.fuzzy.fuzzification import Fuzzification
from fuzzyweather.fuzzy.inference_engine import InferenceEngine
from fuzzyweather.fuzzy.defuzzification import Defuzzification
from fuzzyweather.util.logger import log


class FuzzyInference:
    def __init__(self):
        self.found_when = 0
        self.weather_dic = {}
        self.rain_fall_list = []

    def run(self, when=0):
        fuzzy_set, self.found_when, self.weather_dic, self.rain_fall_list = \
            Fuzzification().get_fuzzy_set_and_crisp_data(when)
        res = InferenceEngine().rule_evaluation(fuzzy_set)
        result_list = Defuzzification().to_crisp_list(res)
        return result_list

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
