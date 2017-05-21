from fuzzyweather.fuzzy import UseDB
from fuzzyweather.fuzzy.membership import Membership


class Defuzzification(UseDB):
    def __init__(self):
        super(Defuzzification, self).__init__()

    def center_of_gravity(self, result):
        mem = self.db.get_after_membership('결과')
        sum_top = 0.
        sum_bottom = 0.
        cog_list = {}
        for t in result:
            for me in mem:
                for m, v in zip(mem[me], result[t]):
                    sum_top += mem[me][m][1] * result[t][v]
                    sum_bottom += result[t][v]
                    if sum_top == 0. or sum_bottom == 0.:
                        sum_result = 0.
                    else:
                        sum_result = sum_top/sum_bottom
                        name = Membership().seek_after_membership(sum_result)
                cog_list[t] = {me: [name, sum_result]}
        return cog_list

# from fuzzyweather.fuzzy.fuzzification import Fuzzification
# from fuzzyweather.fuzzy.rules import Rule
# f = Fuzzification()
# res = Rule().rule_evaluation(f.get_fuzzyset())
# cog = Defuzzification().center_of_gravity(res)
# for c in cog:
#     print(c, cog[c])
