from fuzzyweather.fuzzy import UseDB


class Rule(UseDB):
    def __init__(self):
        super(Rule, self).__init__()
        self.__rule_nums = self.db.get_rule_nums()

    # 전건 평가
    @staticmethod
    def __before_evaluation(rule, time, data, fuzzy_input):
        for r in rule:
            if r.before_not is 1:
                insert = 1. - fuzzy_input[time][r.before_variable][r.before_value]
            else:
                insert = fuzzy_input[time][r.before_variable][r.before_value]
            data[time].append(insert)

    # 전건들의 and, or 평가
    @staticmethod
    def __and_or_evaluation(rule, time, data):
        for r in rule:
            if r.and_field or r.or_field:
                if r.and_field:
                    data[time][1] = data[time][0] if data[time][0] <= data[time][1] else data[time][1]
                else:
                    data[time][1] = data[time][0] if data[time][0] >= data[time][1] else data[time][1]
                del(data[time][0])
            else:
                break
        data[time] = data[time][0]

    # 후건 평가
    @staticmethod
    def __after_evaluation(rule, time, data):
        for r in rule:
            if r.after_variable in ['결과']:
                data[time] = [r.after_value, data[time]]

    # 규칙 평가
    def rule_evaluation(self, fuzzy_input):
        rule_eval_list = {}
        for num in range(1, self.__rule_nums+1):
            data = {}
            rule = self.db.get_rules(num)
            for time, value in fuzzy_input.items():
                data[time] = []
                # 전건
                self.__before_evaluation(rule, time, data, fuzzy_input)
                # AND, OR 처리
                self.__and_or_evaluation(rule, time, data)
                # 후건
                self.__after_evaluation(rule, time, data)
            rule_eval_list[num] = data
        # for r in rule_eval_list:
        #     print(r, rule_eval_list[r].items())
        # 규칙 후건의 통합
        result = self.__rule_after_integration(rule_eval_list)
        return result

    # 규칙 후건의 통합
    @staticmethod
    def __rule_after_integration(eval_list):
        result = {}
        for num in eval_list:
            for time in eval_list[num]:
                eval_element = eval_list[num][time]  # ['언어변수', 값]
                if time not in result:
                    result[time] = {}
                if eval_element[0] not in result[time]:
                    result[time][eval_element[0]] = 0.
                if result[time][eval_element[0]] < eval_element[1]:
                    result[time][eval_element[0]] = eval_element[1]

        return result

# from fuzzyweather.fuzzy.fuzzification import Fuzzification
# f = Fuzzification()
# fs, d = f.get_fuzzyset_and_day(0)
# for f in fs:
#     print(f)
#     for s in fs[f]:
#         print(s, fs[f][s])
# res = Rule().rule_evaluation(fs)
# for r in res:
#     print(r, res[r])
