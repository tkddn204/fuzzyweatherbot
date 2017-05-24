from fuzzyweather.fuzzy import UseDB


class Membership(UseDB):
    def __init__(self):
        super(Membership, self).__init__()
        self._before_mem_data = self.db.get_before_membership()
        self._after_mem_data = self.db.get_after_membership()

    @staticmethod
    def __find_linear_membership(data, ms):
        left, middle, right = ms
        infinite = 99999
        if data <= left or data >= right:
            if left is -infinite or right is infinite:
                value = 1.0
            else:
                value = 0.0
        elif data < middle:
            value = (data - left) / (middle - left)
        elif data == middle:
            value = 1.0
        elif data < right:
            value = (data - right) / (middle - right)
        else:
            value = 0.0
        return value

    def _set_before_membership(self, day_list):
        text = ['밤', '오후', '오전']
        result = {}
        # 밤, 오후, 오전 나눔
        for i, day_ele in enumerate(day_list):
            if day_ele.count(0.0) >= 3:
                continue
            result[text[i]] = {}
            # 구름량, 기온, 습도 순으로 3개 묶음 1개씩 처리
            for day_data, mem in zip(day_ele, self.db.get_before_variables()):
                result[text[i]][mem.variable] = {}
                for key, ms in self._before_mem_data[mem.variable].items():
                    value = self.__find_linear_membership(day_data, ms)
                    result[text[i]][mem.variable][key] = value
        # for a in result.keys():
        #     for d in result[a].keys():
        #             print(a, d, result[a][d])
        return result

    def seek_after_membership(self, value):
        result = ''
        for me in self._after_mem_data:
            temp = 0.
            for after_key, after_value in self._after_mem_data[me].items():
                if temp < self.__find_linear_membership(value, after_value):
                    result = after_key
        return result
