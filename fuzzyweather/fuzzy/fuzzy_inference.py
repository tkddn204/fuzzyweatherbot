from fuzzyweather.fuzzy.fuzzification import Fuzzification
from fuzzyweather.fuzzy.inference_engine import InferenceEngine
from fuzzyweather.fuzzy.defuzzification import Defuzzification
from fuzzyweather.util.logger import log


class FuzzyInference:
    def __init__(self):
        self.output_when = 0
        self.rain_fall = []

    def run(self, when=0):
        fuzzy_set, self.output_when, self.rain_fall = \
            Fuzzification().get_fuzzy_set_and_information(when)
        # log.error(fuzzy_set)
        res = InferenceEngine().rule_evaluation(fuzzy_set)
        # log.error(res)
        cog = Defuzzification().result_text(res)
        return cog

    def test(self, when=0):
        fuzzy_set, self.output_when, self.rain_fall = \
            Fuzzification().get_fuzzy_set_and_information(when)
        log.error(fuzzy_set)
        res = InferenceEngine().rule_evaluation(fuzzy_set)
        log.error(res)
        cog = Defuzzification().result_text(res)
        return cog

# a = FuzzyInference().test(0)
# print(a)
