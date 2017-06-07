from datetime import date
from fuzzyweather.fuzzy import UseDB

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
# font_name = font_manager.FontProperties(fname='NanumGothicLight.ttf').get_name()
#rc('font', family=font_name)
rc('font', family='NanumGothic')
rc('text', usetex='false')


class Graph(UseDB):
    def __init__(self):
        super(Graph, self).__init__()

    def before_draw(self):
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
        # plt.show()

    def after_draw(self):
        fig = plt.figure()
        after = self.db.get_after_membership()
        ax = fig.add_subplot(1, 1, 1)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 1)
        for data in after:
            ax.set_ylabel(data)
            for value, data_list in after[data].items():
                if data_list[0] < 0.0:
                    data_list[0] = -1.0
                elif data_list[2] > 100.0:
                    data_list[2] = 101.0
                print(data_list)
                ran = range(int(data_list[1]) + 2)
                x = [a for a in ran]
                y = [(b - data_list[0]) / (data_list[1] - data_list[0]) for b in ran]
                ax.plot(x, y, color='black')
                ran = range(int(data_list[2]) + 2)
                x2 = [a for a in ran]
                y2 = [(b - data_list[2]) / (data_list[1] - data_list[2]) for b in ran]
                ax.plot(x2, y2, color='black')
        # plt.show()

    def result_file_name(self, res_list, when=0):
        time_list = ['오전', '오후', '밤']
        membership_num = []
        for time in time_list:
            if time in res_list:
                # res_list[time] -> [텍스트, 이모티콘, 수치]'
                membership_num.append(res_list[time][2])

        now = date.today()
        if when is 0:
            img_name = '{0}-today-'.format(now)
        else:
            img_name = '{0}-tomorrow-'.format(now)
        for num in membership_num:
            img_name += '{0:.2f}-'.format(num)

        return img_name[:-1] + '.png'

    def autolabel(self, rects):
        for rect in rects:
            height = rect.get_height()
            if height >= 80:
                text = '매우 좋음'
            elif height >= 60:
                text = '좋음'
            elif height >= 50:
                text = '약간 좋음'
            elif height >= 40:
                text = '보통'
            elif height >= 30:
                text = '약간 나쁨'
            elif height >= 10:
                text = '나쁨'
            elif height > 0:
                text = '매우 나쁨'
            else:
                continue

            plt.text(rect.get_x() + rect.get_width() / 2., height,
                     text,
                     ha='center', va='bottom')
            if height < 96:
                plt.text(rect.get_x() + rect.get_width() / 2., height - 5,
                         '%.1f' % height,
                         ha='center', va='bottom')

    def draw_result_list(self, res_list, img_name='', when=0):
        plt.figure().set_size_inches(5, 6)
        y_membership = []
        time_list = ['오전', '오후', '밤']
        for time in time_list:
            if time in res_list:
                # res_list[time] -> [텍스트, 이모티콘, 수치]'
                y_membership.append(res_list[time][2])
            else:
                y_membership.append(0.0)
        positions = range(1, len(y_membership)+1)

        # 바마다 색깔 지정을 위한 색 지정
        cmap = plt.get_cmap('autumn')

        # 컬러바 지정을 위한 스캐터 생성 후 삭제
        temp_size = range(1, 100)
        plot = plt.scatter(temp_size, temp_size, c=temp_size, cmap=cmap)
        plt.clf()
        color_bar = plt.colorbar(plot, orientation='horizontal', ticks=[1, 50, 99])
        color_bar.ax.set_xticklabels(['매우 나쁨', '보통', '매우 좋음'])

        # 바마다 색깔 지정
        colors = []
        for y_mem in y_membership:
            select_color = y_mem / 100.
            color = cmap(select_color)
            colors.append(color)
        rect = plt.bar(positions, y_membership, color=colors)

        # 컬러바 위치 재지정
        color_bar.ax.set_position([0.11, 0.1, 0.8, 0.19])

        # 바 라벨 지정
        self.autolabel(rect)

        # 틱과 겉 라벨 쓰기
        plt.xticks(positions, time_list)
        plt.ylim(0, 100)
        if when is 0:
            plt.title('오늘의 날씨')
        else:
            plt.title('내일의 날씨')

        path = 'fuzzyweather/fuzzy/result_images/'
        plt.savefig(path+img_name)

# Graph().after_drow()
# res_list1 = {'밤': ['기분 좋은 날씨네요!', ':grinning:', 69.23076923076923]}
# res_list2 = {'밤': ['완전 좋은 날씨에요!', ':satisfied:', 95.0], '오후': ['이정도면 괜찮은 날씨에요!', ':kissing:', 60.0]}
# res_list3 = {'밤': ['완전 좋은 날씨에요!', ':satisfied:', 89.0], '오후': ['이정도면 괜찮은 날씨에요!', ':kissing:', 74.36436], '오전': ['이정도면 괜찮은 날씨에요!', ':kissing:', 52.832]}
# Graph().draw_result_list(res_list1)
