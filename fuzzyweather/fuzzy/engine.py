from fuzzyweather.fuzzy.fuzzification import Fuzzification
from fuzzyweather.fuzzy.rules import Rule
from fuzzyweather.fuzzy.defuzzification import Defuzzification
from fuzzyweather.util.logger import log


class Inference:
    def __init__(self):
        self.day = 0
        self.rain_fall = []

    def run(self, when=0):
        f = Fuzzification(when)
        fuzzy_set, self.day = f.get_fuzzyset_and_day()
        log.error(fuzzy_set)
        self.rain_fall = f.rain_fall
        res = Rule().rule_evaluation(fuzzy_set)
        log.error(res)
        cog = Defuzzification().result_text(res)
        return cog

    def test(self, when=0):
        # f = Fuzzification(when)
        # fuzzy_set, self.day = f.get_fuzzyset_and_day()
        # log.error(fuzzy_set)
        # self.rain_fall = f.rain_fall
        fuzzy_set = {'밤': {'습도': {'매우 습함': 0.0, '건조': 0.0, '습함': 0.0, '쾌적': 0.0, '매우 건조': 1.0}, '기온': {'적당함': 0.0, '추움': 0.0, '서늘함': 0.0, '따뜻함': 0.0, '더움': 0.9998499234609651, '매우 추움': 0.0}, '구름량': {'구름 많음': 0.0, '맑음': 0.0, '구름 조금': 0.33333333333333337, '흐림': 0.0, '흐리고 비': 0.0}}, '오후': {'습도': {'매우 습함': 0.0, '건조': 0.3333333333333333, '습함': 0.0, '쾌적': 0.0, '매우 건조': 0.5}, '기온': {'적당함': 0.0, '추움': 0.0, '서늘함': 0.0, '따뜻함': 0.0, '더움': 1.0, '매우 추움': 0.0}, '구름량': {'구름 많음': 1.0, '맑음': 0.0, '구름 조금': 0.0, '흐림': 0.0, '흐리고 비': 0.0}}}
        res = Rule().rule_evaluation(fuzzy_set)
        log.error(res)
        cog = Defuzzification().result_text(res)
        return cog

# a = Inference().run(0)
# print(a)
