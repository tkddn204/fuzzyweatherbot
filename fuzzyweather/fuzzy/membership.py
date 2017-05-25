from fuzzyweather.fuzzy import UseDB


class Membership(UseDB):
    def __init__(self):
        super(Membership, self).__init__()
        self._before_mem_data = self.db.get_before_membership()
        self._after_mem_data = self.db.get_after_membership()

    @staticmethod
    def __find_linear_membership(data, value_membership):
        left, middle, right = value_membership
        infinite = 99999
        if data <= left or data >= right:
            if left is -infinite or right is infinite:
                membership_of_value = 1.0
            else:
                membership_of_value = 0.0
        elif data < middle:
            membership_of_value = (data - left) / (middle - left)
        elif data == middle:
            membership_of_value = 1.0
        elif data < right:
            membership_of_value = (data - right) / (middle - right)
        else:
            membership_of_value = 0.0
        return membership_of_value

    def _set_crisp_membership(self, split_time_list):
        time = ['밤', '오후', '오전']
        result = {}
        # 밤, 오후, 오전 나눔
        for time_index, time_value in enumerate(split_time_list):
            if time_value.count(0.0) >= 3:
                continue
            result[time[time_index]] = {}
            # 구름량, 기온, 습도 순으로 3개 묶음 1개씩 처리
            for index, before in enumerate(self.db.get_before_variables()):
                result[time[time_index]][before.variable] = {}
                for value, value_membership in self._before_mem_data[before.variable].items():
                    found_value = self.__find_linear_membership(time_value[index], value_membership)
                    result[time[time_index]][before.variable][value] = found_value
        # for a in result.keys():
        #     for d in result[a].keys():
        #             print(a, d, result[a][d])
        return result

    def seek_after_membership(self, value):
        result = ''
        temp = 0.
        for me in self._after_mem_data:
            for after_key, after_value in self._after_mem_data[me].items():
                if temp < self.__find_linear_membership(value, after_value):
                    result = after_key
        return result
