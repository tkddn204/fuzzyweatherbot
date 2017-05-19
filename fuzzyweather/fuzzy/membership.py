
INFINITE = 99999


class Membership:
    def __init__(self, variable):
        self.variable = variable
        self.membership = {}

    def make_linear_fit(self, name, left=0., right=0.):
        # 대입하는 값들은 X축임
        self.membership['name'] = name
        self.membership['name']['left'] = left
        self.membership['name']['right'] = right

    def all_make_linear_fit(self, *fit):
        for f in fit:
            self.make_linear_fit(self, f[0], f[1], f[2])

    def seek_membership(self, name, value=0.):
        # y축을 계산함
        left = self.membership['name']['left']
        right = self.membership['name']['right']
        middle = (left + right) / 2.

        if value <= left or value >= right:
            if left is -INFINITE or right is INFINITE:
                return 1.0
            return 0.0
        elif value < middle:
            if left is -INFINITE:
                return 1.0
            else:
                return (value - left) / (middle - left)
        elif value < right:
            if right is INFINITE:
                return 1.0
            else:
                return (value - right) / (middle - right)
        elif value == middle:
            return 1.0
        else:
            return 0.0

