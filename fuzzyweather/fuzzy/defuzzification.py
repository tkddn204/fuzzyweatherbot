from fuzzyweather.fuzzy import UseDB
from fuzzyweather.fuzzy.membership import Membership


class Defuzzification(UseDB):
    def __init__(self):
        super(Defuzzification, self).__init__()

    # 무게중심법 계산
    def __center_of_gravity(self, result):
        mem = self.db.get_after_membership()
        sum_top = 0.
        sum_bottom = 0.
        cog_list = {}
        for time in result:
            for me in mem:
                for m in mem[me]:  # 여기가 문제였네!
                    sum_top += mem[me][m][1] * result[time][m]
                    sum_bottom += result[time][m]
                sum_result = sum_top/sum_bottom if sum_top == 0. or sum_bottom == 0. else 0.
                after_mem = Membership().seek_after_membership(sum_result)
                cog_list[time] = {me: [after_mem[0], sum_result]}
        return cog_list

    # 결과를 텍스트로 내보내기
    def result_text(self, result):
        cog_list = self.__center_of_gravity(result)
        after_list = self.db.get_after_text_and_emoticon()
        result = {}
        for time in cog_list:  # 언제
            for r in cog_list[time]:  # 결과
                for after in after_list:
                    if cog_list[time][r][0] == after.value:
                        result[time] = [after.text, after.emoticon, cog_list[time][r][1]]
        return result

# from fuzzyweather.fuzzy.fuzzification import Fuzzification
# from fuzzyweather.fuzzy.rules import Rule
# f = Fuzzification()
# res = Rule().rule_evaluation(f.get_fuzzyset())
# cog = Defuzzification().result_text(res)
# for c in cog:
#     print(c)
