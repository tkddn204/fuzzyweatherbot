from fuzzyweather.fuzzy.fuzzification import Fuzzification
from fuzzyweather.fuzzy.rules import Rule
from fuzzyweather.fuzzy.defuzzification import Defuzzification


class Inference(Fuzzification):
    def __init__(self):
        super(Inference, self).__init__()

    def run(self, day=0):
        f = Fuzzification(day)
        res = Rule().rule_evaluation(f.get_fuzzyset())
        cog = Defuzzification().result_text(res)
        return cog
