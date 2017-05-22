from fuzzyweather.fuzzy import UseDB
from fuzzyweather.fuzzy.membership import Membership


class Defuzzification(UseDB):
    def __init__(self):
        super(Defuzzification, self).__init__()

    # 무게중심법 계산
    def __center_of_gravity(self, result):
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
                cog_list[t] = {me: [name[0], sum_result]}
        return cog_list

    # 결과를 텍스트로 내보내기
    def result_text(self, result):
        cog_list = self.__center_of_gravity(result)
        after_list = self.db.get_after_text()
        result = {}
        for d in cog_list:
            for r in cog_list[d]:
                for after in after_list:
                    if cog_list[d][r][0] == after.value:
                        result[d] = [r, after.text, cog_list[d][r][1]]
        return result

# from fuzzyweather.fuzzy.fuzzification import Fuzzification
# from fuzzyweather.fuzzy.rules import Rule
# f = Fuzzification()
# res = Rule().rule_evaluation(f.get_fuzzyset())
# cog = Defuzzification().result_text(res)
# for c in cog:
#     print(c)
