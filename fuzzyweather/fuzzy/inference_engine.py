from fuzzyweather.fuzzy import UseDB


class InferenceEngine(UseDB):
    def __init__(self):
        super(InferenceEngine, self).__init__()

    # 규칙 평가
    def rule_evaluation(self, fuzzy_input):
        rule_nums = self.db.get_rule_nums()
        after_variables = self.db.get_after_variables()
        evaluated_data_dic = {}
        for rule_num in range(1, rule_nums+1):
            handling_data = {}
            current_rule = self.db.get_rule(rule_num)

            # 전건 평가 -> 전건 and, or 처리 -> 후건 평가
            for time, fuzzy_input_value in fuzzy_input.items():
                self.__before_evaluation(current_rule, time, handling_data, fuzzy_input_value)
                self.__and_or_evaluation(current_rule, time, handling_data)
                self.__after_evaluation(current_rule, time, handling_data, after_variables)

            evaluated_data_dic[rule_num] = handling_data
        # 규칙 후건의 통합
        result = self.__rule_after_integration(evaluated_data_dic)
        return result

    # 전건 평가
    @staticmethod
    def __before_evaluation(current_rule, time, handling_data, fuzzy_input_value):
        handling_data[time] = []
        for rule_row in current_rule:
            if rule_row.before_not is 1:
                insert = 1. - fuzzy_input_value[rule_row.before_variable][rule_row.before_value]
            else:
                insert = fuzzy_input_value[rule_row.before_variable][rule_row.before_value]
            handling_data[time].append(insert)

    # 전건들의 and, or 처리
    @staticmethod
    def __and_or_evaluation(current_rule, time, handling_data):
        for rule_row in current_rule:
            before_data_list = handling_data[time]
            if rule_row.and_field is 1:
                if before_data_list[0] <= before_data_list[1]:
                    before_data_list[1] = before_data_list[0]
            elif rule_row.or_field is 1:
                if before_data_list[0] >= before_data_list[1]:
                    before_data_list[1] = before_data_list[0]
            else:
                # 더 이상 처리할 게 없음
                break
            del(before_data_list[0])

    # 후건 평가
    @staticmethod
    def __after_evaluation(current_rule, time, handling_data, after_variables):
        for rule_row in current_rule:
            if rule_row.after_variable in after_variables:
                # 원래 전건 평가했던 데이터를 후언어값과 함께 집어넣음
                handling_data[time] = [rule_row.after_value, handling_data[time][0]]

    # 규칙 후건의 통합
    @staticmethod
    def __rule_after_integration(evaluated_data_dic):
        result = {}
        for rule_num in evaluated_data_dic:
            for time in evaluated_data_dic[rule_num]:
                # eval_element -> ['언어변수', 값]
                eval_element = evaluated_data_dic[rule_num][time]
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
