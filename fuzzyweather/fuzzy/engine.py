from fuzzyweather.fuzzy.fuzzification import Fuzzification
from fuzzyweather.fuzzy.rules import Rule
from fuzzyweather.fuzzy.defuzzification import Defuzzification


class Inference(Fuzzification):
    def __init__(self):
        super(Inference, self).__init__()
        self.day = 0

    def run(self, when=0):
        f = Fuzzification(when)
        fuzzyset, self.day = f.get_fuzzyset_and_day()
        res = Rule().rule_evaluation(fuzzyset)
        cog = Defuzzification().result_text(res)
        return cog
