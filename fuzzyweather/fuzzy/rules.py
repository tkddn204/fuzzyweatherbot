from fuzzyweather.fuzzy import UseDB


class Rule(UseDB):
    def __init__(self):
        super(Rule, self).__init__()

        self.__rule_nums = self.db.get_rule_nums()
        self.__rule = self.db.get_rules(1)

    # 전건 평가
    def __before_evaluation(self, d, data, fuzzy_input):
        for r in self.__rule:
            if r.before_not:
                data[d].append(1. - fuzzy_input[d][r.before_variable][r.before_value])
            else:
                data[d].append(fuzzy_input[d][r.before_variable][r.before_value])

    # 전건들의 and, or 평가
    def __and_or_evaluation(self, d, data):
        for r in self.__rule:
            if r.and_field or r.or_field:
                for i in range(len(data[d]) - 1):
                    if r.and_field:
                        data[d][i] = data[d][i] if data[d][i] > data[d][i + 1] else data[d][i + 1]
                    else:
                        data[d][i] = data[d][i] if data[d][i] < data[d][i + 1] else data[d][i + 1]
                    del (data[d][i + 1])
            else:
                break

    # 후건 평가
    def __after_evaluation(self, d, data):
        for r in self.__rule:
            if r.after_variable in ['결과']:
                data[d] = [r.after_value, data[d][0]]

    # 규칙 평가
    def rule_evaluation(self, fuzzy_input):
        rule_eval_list = {}
        for num in range(1, self.__rule_nums+1):
            data = {}
            self.__rule = self.db.get_rules(num)
            for d in fuzzy_input.keys():
                data[d] = []
                # 전건
                self.__before_evaluation(d, data, fuzzy_input)
                # AND, OR 처리
                self.__and_or_evaluation(d, data)
                # 후건
                self.__after_evaluation(d, data)
            rule_eval_list[num] = data
        # for r in rule_eval_list:
        #     print(r, rule_eval_list[r].keys())
        # 규칙 후건의 통합
        result = self.__rule_after_integration(rule_eval_list)
        return result

    # 규칙 후건의 통합
    @staticmethod
    def __rule_after_integration(eval_list):
        result = {}
        for r in eval_list:
            for d in eval_list[r]:
                eval_element = eval_list[r][d]
                if d not in result:
                    result[d] = {}
                if eval_element[0] not in result[d]:
                    result[d][eval_element[0]] = 0.
                if result[d][eval_element[0]] < eval_element[1]:
                    result[d][eval_element[0]] = eval_element[1]
        return result

# from fuzzyweather.fuzzy.fuzzification import Fuzzification
# f = Fuzzification()
# res = Rule().rule_evaluation(f.get_fuzzyset())
# for r in res:
#     print(res[r])

