import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)
from fuzzyweather.fuzzy import UseDB


class Graph(UseDB):
    def __init__(self):
        super(Graph, self).__init__()

    def draw(self):
        fig = plt.figure()
        before = self.db.get_before_membership()
        for i, [variable, data] in enumerate(before.items()):
            ax = fig.add_subplot(3, 1, i+1)
            if '기온' not in variable:
                ax.set_xlim(0, 100)
            else:
                ax.set_xlim(0, 50)
            ax.set_ylim(0, 1)
            ax.set_ylabel(variable)
            for value, data_list in data.items():
                if data_list[0] < 0.0:
                    data_list[0] = -1.0
                elif data_list[2] > 100.0:
                    data_list[2] = 100.0
                print(data_list)
                ran = range(int(data_list[1])+2)
                x = [a for a in ran]
                y = [(b-data_list[0])/(data_list[1]-data_list[0]) for b in ran]
                ax.plot(x, y, color='black')
                ran = range(int(data_list[2])+2)
                x2 = [a for a in ran]
                y2 = [(b-data_list[2])/(data_list[1]-data_list[2]) for b in ran]
                ax.plot(x2, y2, color='black')
        plt.show()

Graph().draw()
