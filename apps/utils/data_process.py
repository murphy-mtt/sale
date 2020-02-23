from django.apps import apps
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from matplotlib.patches import ConnectionPatch
from matplotlib.ticker import MaxNLocator
from collections import namedtuple

from django.conf import settings


plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


# GLOBAL CONSTANTS
category_dict = {
    "area": "大区",
    "cancer": "肿瘤类型",
    "department": "科室",
    "sample_type": "样本方式",
    "order_type": "订单类型",
    "product_type": "产品",
    "doctor": "送检医生",
}


class DataProcessor:
    def __init__(self, file_path=None, dataframe=None):
        self.file_path = file_path
        self.dataframe = dataframe

    def one_dimension(self, index, value, aggfunc=np.sum):
        if not index:
            raise ValueError("Need index.")
        return pd.pivot_table(self.dataframe, index=index, values=value, aggfunc=aggfunc)

    def two_dimension(self, index, value, aggfunc=np.sum):
        pass

    def multi_columns(self, index, columns, values=['price'], aggfunc=np.sum):
        return pd.pivot_table(self.dataframe, index=index, columns=columns, values=values, aggfunc=aggfunc).fillna(0)


class Graph:
    def __init__(self, nrows=1, ncols=1, savefig_path=None, title=None, figsize=None):
        if figsize:
            self.fig, self.ax_list = plt.subplots(
                nrows=nrows,
                ncols=ncols,
                figsize=figsize,
            )
        else:
            self.fig, self.ax_list = plt.subplots(
                nrows=nrows,
                ncols=ncols,
            )
        self.savefig_path = savefig_path
        self.title = title

    def callback(self, graph_type, plt_args, *args):
        method = getattr(self, graph_type, None)
        if callable(method):
            method(*args)
        plt.setp(plt_args)
        plt.title(self.title)
        plt.savefig(self.savefig_path)

    def bar(self, df, ax, fold=None, category=None, label_fs=8):
        if fold:
            df = df/fold
        x = np.arange(len(df))
        x_label = df.index.values.tolist()
        y = df.iloc[:, 0].values.tolist()
        rects = ax.bar(x, y, alpha=0.5)
        ax.set_xticks(x)
        ax.set_xticklabels(x_label, rotation=-45, ha='left', fontsize=label_fs)
        ax.set_ylim(0, max(y)*1.1)
        if fold:
            ylabel = "销量（x{}）".format(str(fold))
        else:
            ylabel = "销量"
        ax.set_ylabel(ylabel, fontsize=label_fs)

        if category:
            title = "销量分布（按{}）".format(category[df.index.name])
        else:
            title = "{}".format(df.index.name)
        ax.set_title(title)
        self.autolabel(ax, rects)
        return rects

    def pie(self, df, ax):
        pass

    def stacked_plot(self, data):
        fig, ax = self.fig, self.ax_list
        df = data
        xtickslabel = df.index.strftime(date_format='%Y-%m')
        x = np.arange(len(df.index))
        y = []
        for i in range(len(df.columns)):
            # use map to convert str into float
            y.append(df.iloc[:, i].map(lambda j: float(j)))
        xticks = range(0, len(df.index), 1)
        ax.set_xticks(xticks)
        ax.stackplot(x, y, labels=df.columns.levels[1])
        ax.set_xticklabels(xtickslabel, rotation=45)
        plt.legend(loc='upper left')

    def ranking_bar(self, s, df_ps, df_total):
        Student = namedtuple('Student', ['name', 'grade', 'gender'])
        Score = namedtuple('Score', ['score', 'percentile'])
        result = {}

        for sale in df_ps.columns:
            result[sale[1]] = {}
            scoreList = []
            percList = []
            result[sale[1]]['s'] = []
            result[sale[1]]['p'] = []
            for product in df_ps.index:
                product_total_sale = df_ps.loc[product, :].values.tolist()
                product_individual_sale = df_ps.loc[product, sale]
                percentile = stats.percentileofscore(product_total_sale, product_individual_sale)
                scoreList.append(product_individual_sale)
                percList.append(percentile)
                result[sale[1]]['s'] = scoreList
                result[sale[1]]['p'] = percList

        testNames, testMeta = self.get_product_list(df_total)
        # testNames = [i.replace("（", "\n（") for i in testNames]
        student = Student(s, 2, 'boy')
        cohort_size = len(df_ps.columns.levels[1])
        scores = dict(zip(testNames, (Score(v, p) for v, p in zip(result[s]['s'], result[s]['p']))))
        arts = self.plot_student_results(student, scores, cohort_size, testNames, testMeta)
        plt.savefig(self.savefig_path)

    def plot_student_results(self, student, scores, cohort_size, testNames, testMeta):
        for i in range(len(testNames)):
            testMeta.append("")

        #  create the figure
        fig, ax1 = plt.subplots(figsize=(21, 7))
        fig.subplots_adjust(left=0.115, right=0.88)
        fig.canvas.set_window_title('Eldorado K-8 Fitness Chart')

        pos = np.arange(len(testNames))

        rects = ax1.barh(pos, [scores[k].percentile for k in testNames],
                         align='center',
                         height=0.5,
                         tick_label=testNames)

        ax1.set_title(student.name)

        ax1.set_xlim([0, 100])
        ax1.xaxis.set_major_locator(MaxNLocator(11))
        ax1.xaxis.grid(True, linestyle='--', which='major',
                       color='grey', alpha=.25)

        # Plot a solid vertical gridline to highlight the median position
        ax1.axvline(50, color='grey', alpha=0.25)

        # Set the right-hand Y-axis ticks and labels
        ax2 = ax1.twinx()

        scoreLabels = [self.format_score(scores[k].score, k, testNames, testMeta) for k in testNames]

        # set the tick locations
        ax2.set_yticks(pos)
        # make sure that the limits are set equally on both yaxis so the
        # ticks line up
        ax2.set_ylim(ax1.get_ylim())

        # set the tick labels
        ax2.set_yticklabels(scoreLabels)

        ax2.set_ylabel('Test Scores')

        xlabel = ('销售业绩在全国范围内排名百分位数\n'
                  '人数: {cohort_size}')
        ax1.set_xlabel(xlabel.format(grade=self.attach_ordinal(student.grade),
                                     gender=student.gender.title(),
                                     cohort_size=cohort_size))

        rect_labels = []
        # Lastly, write in the ranking inside each bar to aid in interpretation
        for rect in rects:
            # Rectangle widths are already integer-valued but are floating
            # type, so it helps to remove the trailing decimal point and 0 by
            # converting width to int type
            width = int(rect.get_width())

            rankStr = self.attach_ordinal(width)
            # The bars aren't wide enough to print the ranking inside
            if width < 40:
                # Shift the text to the right side of the right edge
                xloc = 5
                # Black against white background
                clr = 'black'
                align = 'left'
            else:
                # Shift the text to the left side of the right edge
                xloc = -5
                # White on magenta
                clr = 'white'
                align = 'right'

            # Center the text vertically in the bar
            yloc = rect.get_y() + rect.get_height() / 2
            label = ax1.annotate(rankStr, xy=(width, yloc), xytext=(xloc, 0),
                                 textcoords="offset points",
                                 ha=align, va='center',
                                 color=clr, weight='bold', clip_on=True)
            rect_labels.append(label)

        # make the interactive mouse over give the bar title
        ax2.fmt_ydata = self.format_ycursor
        # return all of the artists created

        return {'fig': fig,
                'ax': ax1,
                'ax_right': ax2,
                'bars': rects,
                'perc_labels': rect_labels}

    def bar_of_pie(self, data):
        fig, (ax1, ax2) = self.fig, self.ax_list
        fig.subplots_adjust(wspace=0)

        ratios1, label1, ratios2, label2 = data

        # pie chart parameters
        explode = np.zeros(len(ratios1))
        explode[0] = 0.1
        # rotate so that first wedge is split by the x-axis
        angle = -180 * ratios1[0]
        ax1.pie(ratios1, autopct='%1.1f%%', startangle=angle,
                labels=label1, explode=explode)

        # bar chart parameters
        xpos = 0
        bottom = 0
        width = .2
        # colors = [[.1, .3, .5], [.1, .3, .3], [.1, .3, .7], [.1, .3, .9]]

        for j in range(len(ratios2)):
            height = ratios2[j]
            ax2.bar(xpos, height, width, bottom=bottom)
            ypos = bottom + ax2.patches[j].get_height() / 2
            bottom += height
            ax2.text(xpos, ypos, "%d%%" % (ax2.patches[j].get_height() * 100),
                     ha='center')

        ax2.legend(label2)
        ax2.axis('off')
        ax2.set_xlim(- 2.5 * width, 2.5 * width)

        # use ConnectionPatch to draw lines between the two plots
        # get the wedge data
        theta1, theta2 = ax1.patches[0].theta1, ax1.patches[0].theta2
        center, r = ax1.patches[0].center, ax1.patches[0].r
        bar_height = sum([item.get_height() for item in ax2.patches])

        # draw top connecting line
        x = r * np.cos(np.pi / 180 * theta2) + center[0]
        y = np.sin(np.pi / 180 * theta2) + center[1]
        con = ConnectionPatch(xyA=(- width / 2, bar_height), xyB=(x, y),
                              coordsA="data", coordsB="data", axesA=ax2, axesB=ax1)
        con.set_color([0, 0, 0])
        con.set_linewidth(1)
        ax2.add_artist(con)

        # draw bottom connecting line
        x = r * np.cos(np.pi / 180 * theta1) + center[0]
        y = np.sin(np.pi / 180 * theta1) + center[1]
        con = ConnectionPatch(xyA=(- width / 2, 0), xyB=(x, y), coordsA="data",
                              coordsB="data", axesA=ax2, axesB=ax1)
        con.set_color([0, 0, 0])
        ax2.add_artist(con)
        con.set_linewidth(1)
        # return {
        #     'fig': fig,
        #     'ax1': ax1,
        #     # 'ax2': ax2,
        #     # 'con': con,
        #     # 'theta1': theta1,
        #     # 'theta2': theta2,
        # }

    def bar_with_table_graph(self, data):
        fig, ax = self.fig, self.ax_list

        index = data.index
        columns = data.columns

        colors = plt.cm.BuPu(np.linspace(0, 0.5, len(index)))

        # Get some pastel shades for the colors
        n_rows = len(data)

        index = np.arange(len(columns)) + 0.3
        bar_width = 0.4

        # Initialize the vertical-offset for the stacked bar chart.
        y_offset = np.zeros(len(columns))

        # Plot bars and create text labels for the table
        cell_text = []
        for row in range(n_rows):
            plt.bar(index, data.iloc[row, :], bar_width, bottom=y_offset, color=colors[row])
            y_offset = y_offset + data.iloc[row, :]
            cell_text.append(['%1.1f' % (x / 1000.0) for x in y_offset])
        # Reverse colors and text labels to display the last value at the top.
        colors = colors[::-1]
        cell_text.reverse()

        # Add a table at the bottom of the axes
        the_table = plt.table(cellText=cell_text,
                              rowLabels=data.index,
                              rowColours=colors,
                              colLabels=data.columns,
                              loc='bottom')

        # Adjust layout to make room for the table:
        plt.subplots_adjust(left=0.2, bottom=0.2)

        plt.ylabel("销售额")
        plt.xticks([])

    @staticmethod
    def autolabel(ax, rects):
        """
        Attach a text label above each bar in *rects*, displaying its height.
        :param ax:
        :param rects:
        :return:
        """
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    @staticmethod
    def attach_ordinal(num):
        """
        helper function to add ordinal string to integers

        1 -> 1st
        56 -> 56th
        """
        suffixes = {str(i): v
                    for i, v in enumerate(['th', 'st', 'nd', 'rd', 'th',
                                           'th', 'th', 'th', 'th', 'th'])}

        v = str(num)
        # special case early teens
        if v in {'11', '12', '13'}:
            return v + 'th'
        return v + suffixes[v[-1]]

    def format_score(self, scr, test, testNames, testMeta):
        """
        Build up the score labels for the right Y-axis by first
        appending a carriage return to each string and then tacking on
        the appropriate meta information (i.e., 'laps' vs 'seconds'). We
        want the labels centered on the ticks, so if there is no meta
        info (like for pushups) then don't add the carriage return to
        the string
        """
        # md = testMeta[test]
        md = ""
        if md:
            return '{0}\n{1}'.format(scr, md)
        else:
            return scr

    @staticmethod
    def format_ycursor(y):
        y = int(y)
        if y < 0 or y >= len(testNames):
            return ''
        else:
            return testNames[y]

    @staticmethod
    def get_product_list(df):
        df_ps = pd.pivot_table(df, index=['product_type'], columns=['sale_person'], aggfunc=sum).fillna(0)
        product_name = df_ps.index.values.tolist()
        testMeta = []
        for i in range(len(product_name)):
            testMeta.append("")
        return product_name, testMeta

    @staticmethod
    def product_change_line(products):
        return

    @staticmethod
    def percent_convert(ser):
        return ser / float(ser.sum())


class Chandler:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def index_graph(self, category):
        ncols = 3
        nrows = int(np.ceil(len(category)/ncols))
        graph = Graph(
            nrows=nrows,
            ncols=ncols,
            savefig_path="/home/murphy/sale/static/images/stat.png",
            figsize=(15, 10),
        )
        data_processor = DataProcessor(dataframe=self.dataframe)
        df_list = [data_processor.one_dimension(index=i, value='price', aggfunc=np.sum) for i in category]
        for i in range(len(df_list), ncols*nrows):
            df_list.insert(i, None)
        ind = 0
        for i in range(nrows):
            for j in range(ncols):
                d = df_list[ind]
                ax = graph.ax_list[i][j]
                if "None" not in str(type(d)):
                    graph.callback("bar", {'alpha': 0.3}, d, ax, 1000, category_dict, 7)
                ind += 1

    def area_region_bar_graph(self):
        pass

    def sale_rank_graph(self):
        pass

    def sale_bar_graph(self, category):
        ncols = 2
        nrows = int(np.ceil(len(category)/ncols))
        data_processor = DataProcessor(dataframe=self.dataframe)
        graph = Graph(
            nrows=nrows,
            ncols=ncols,
            savefig_path="/home/murphy/sale/static/images/saleman_bar.png",
            figsize=(10, 10),
        )
        df_list = [data_processor.one_dimension(index=i, value='price', aggfunc=np.sum) for i in category]
        for i in range(len(df_list), ncols*nrows):
            df_list.insert(i, None)
        ind = 0
        for i in range(nrows):
            for j in range(ncols):
                d = df_list[ind]
                ax = graph.ax_list[i][j]
                if "None" not in str(type(d)):
                    try:
                        graph.callback("bar", {'alpha': 0.3}, d, ax, 1000, category, 7)
                    except:
                        pass
                ind += 1

    def sale_ranking_graph(self, dataframe, s):
        data_processor = DataProcessor(dataframe=dataframe)
        graph = Graph(savefig_path="/home/murphy/sale/static/images/saleman_ranking.png")
        df_ps = data_processor.multi_columns(index=['product_type'], columns=['sale_person'])
        graph.ranking_bar(s, df_ps, dataframe)

    def region_distribution(self, region=None):
        df = self.dataframe
        df_bp = pd.pivot_table(df, index=['region', 'sale_person'], values=['price'], aggfunc=np.sum).fillna(0)
        graph = Graph(
            nrows=1,
            ncols=2,
            title="区域销量分布：{}".format(region),
            savefig_path="/home/murphy/sale/static/images/region_distribution.png"
        )
        counts1 = []
        lables1 = df_bp.index.levels[0].values.tolist()
        region_index = lables1.index(region)
        item = lables1.pop(region_index)
        lables1.insert(0, item)
        for i in lables1:
            counts1.append(df_bp.loc[i].sum()[0])
        counts1 = graph.percent_convert(np.array(counts1))
        count2 = graph.percent_convert(df_bp.loc[region].values)
        labels2 = df_bp.loc[region].index.tolist()
        data = [counts1, lables1, count2, labels2]
        graph.callback('bar_of_pie', {}, data)

    def region_stacked_graph(self):
        df_tmp = self.dataframe
        p = ["%s-%s" % (a.year, a.month) for a in df_tmp['create_date']]
        df_tmp['period'] = pd.to_datetime(p, format='%Y-%m')
        df_filled = pd.pivot_table(
            df_tmp,
            index=['period'],
            values=['price'],
            columns=['region'],
            aggfunc=np.sum).fillna(value=0.00).applymap("{0:.02f}".format)
        graph = Graph(
            title="区域销量分布堆积图(按月份统计)",
            savefig_path="/home/murphy/sale/static/images/region_stacked_graph.png",
        )
        graph.callback('stacked_plot', {}, df_filled)

    def name_pending(self):
        """
        堆积条形图结合数据表
        :return:
        """
        data = self.dataframe
        graph = Graph(
            savefig_path=os.path.join(settings.BASE_DIR, 'static/images/bar_with_table_graph.png'),
            title="Test"
        )
        graph.callback('bar_with_table_graph', {}, data)
