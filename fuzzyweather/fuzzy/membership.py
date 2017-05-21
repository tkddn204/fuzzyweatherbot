from fuzzyweather.fuzzy import UseDB
from fuzzyweather.util.timer import get_season

INFINITE = 99999


class Membership(UseDB):
    def __init__(self):
        super(Membership, self).__init__()
        self._mem_data = self.db.get_membership(get_season(), '기온', '습도')

    def _set_membership(self, day):
        result = {}
        for i, d in enumerate(day):
            if 0 not in d:
                result[i] = {}
                for rd, mem in zip(d, self._mem_data.keys()):
                    result[i][mem] = []
                    for m in self._mem_data[mem].keys():
                        value_name = m
                        left = self._mem_data[mem][m][0]
                        middle = self._mem_data[mem][m][1]
                        right = self._mem_data[mem][m][2]
                        if rd <= left or rd >= right:
                            if left is -INFINITE or right is INFINITE:
                                value = 1.0
                            else:
                                value = 0.0
                        elif rd < middle:
                            value = (rd - left) / (middle - left)
                        elif rd == middle:
                            value = 1.0
                        elif rd < right:
                            value = (rd - right) / (middle - right)
                        else:
                            value = 0.0
                        result[i][mem].append([value_name, value])
        # for a in result.keys():
        #     for d in result[a].keys():
        #         print(result[a][d])
        return result
