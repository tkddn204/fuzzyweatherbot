from fuzzyweather.fuzzy import UseDB
from fuzzyweather.fuzzy.membership import Membership


class Defuzzification(UseDB):
    def __init__(self):
        super(Defuzzification, self).__init__()

    # 무게중심법 계산
    def __center_of_gravity(self, result):
        after_membership = self.db.get_after_membership()
        cog_list = {}
        for time in result:
            for after_variable in after_membership:
                sum_top = 0.
                sum_bottom = 0.
                for after_value in after_membership[after_variable]:  # 여기가 문제였네!
                    sum_top += after_membership[after_variable][after_value][1]\
                               * result[time][after_value]
                    sum_bottom += result[time][after_value]
                sum_result = 0. if sum_top == 0. or sum_bottom == 0. else sum_top/sum_bottom
                after_mem = Membership().seek_after_membership(sum_result)
                cog_list[time] = {after_variable: [after_mem, sum_result]}
        return cog_list

    # 결과를 crisp한 리스트로 내보내기
    def to_crisp_list(self, result):
        cog_list = self.__center_of_gravity(result)
        after_list = self.db.get_after_text_and_emoticon()
        result = {}
        for time in cog_list:  # 언제
            for after_value in cog_list[time]:  # 결과
                for after in after_list:
                    if cog_list[time][after_value][0] == after.value:
                        result[time] = [after.text, after.emoticon,
                                        cog_list[time][after_value][1]]
        return result

# from fuzzyweather.fuzzy.fuzzification import Fuzzification
# from fuzzyweather.fuzzy.rules import Rule
# f = Fuzzification()
# res = Rule().rule_evaluation(f.get_fuzzyset())
# cog = Defuzzification().to_crisp_list(res)
# for c in cog:
#     print(c)
