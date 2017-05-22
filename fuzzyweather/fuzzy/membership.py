from fuzzyweather.fuzzy import UseDB
from fuzzyweather.util.timer import get_season

INFINITE = 99999
TIME_LIST = ['밤', '오후', '오전']


class Membership(UseDB):
    def __init__(self):
        super(Membership, self).__init__()
        self._before_mem_data = self.db.get_before_membership(get_season(), '기온', '습도')
        self._after_mem_data = self.db.get_after_membership('결과')

    @staticmethod
    def __find_linear_membership(data, left, middle, right):
        if data <= left or data >= right:
            if left is -INFINITE or right is INFINITE:
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

    def _set_before_membership(self, day):
        result = {}
        for i, d in enumerate(day):
            if 0 not in d:
                result[TIME_LIST[i]] = {}
                for rd, mem in zip(d, self._before_mem_data.keys()):
                    result[TIME_LIST[i]][mem] = {}
                    for m in self._before_mem_data[mem].keys():
                        left = self._before_mem_data[mem][m][0]
                        middle = self._before_mem_data[mem][m][1]
                        right = self._before_mem_data[mem][m][2]
                        value = self.__find_linear_membership(rd, left, middle, right)
                        result[TIME_LIST[i]][mem][m] = value
        # for a in result.keys():
        #     for d in result[a].keys():
        #         print(result[a][d])
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
