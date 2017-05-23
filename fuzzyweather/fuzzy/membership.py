from fuzzyweather.fuzzy import UseDB


class Membership(UseDB):
    def __init__(self):
        super(Membership, self).__init__()
        self._before_mem_data = self.db.get_before_membership()
        self._after_mem_data = self.db.get_after_membership()

    @staticmethod
    def __find_linear_membership(data, left, middle, right):
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
        for i, day in enumerate(day_list):
            if 0 not in day:
                result[text[i]] = {}
                # 기온, 3개 묶음 1개씩 처리
                for day_data, mem in zip(day, self._before_mem_data.keys()):
                    result[text[i]][mem] = {}
                    for m in self._before_mem_data[mem].keys():
                        left = self._before_mem_data[mem][m][0]
                        middle = self._before_mem_data[mem][m][1]
                        right = self._before_mem_data[mem][m][2]
                        value = self.__find_linear_membership(day_data, left, middle, right)
                        result[text[i]][mem][m] = value
        # for a in result.keys():
        #     for d in result[a].keys():
        #         for k in result[a][k].keys():
        #             print(result[a][d][k])
        return result

    def seek_after_membership(self, value):
        result = []
        for me in self._after_mem_data:
            temp = []
            mem_data_keys = list(self._after_mem_data[me].keys())
            for m in self._after_mem_data[me]:
                temp.append(self.__find_linear_membership(value,
                                                          self._after_mem_data[me][m][0],
                                                          self._after_mem_data[me][m][1],
                                                          self._after_mem_data[me][m][2]))
            result.append(mem_data_keys[temp.index(max(temp))])

        return result
