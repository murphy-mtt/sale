from django.apps import apps
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from matplotlib.patches import ConnectionPatch
from matplotlib.ticker import MaxNLocator
from collections import namedtuple


plt.rcParams['font.sans-serif'] = ['SimSun']
plt.rcParams['axes.unicode_minus'] = False


# GLOBAL CONSTANTS
category_dict = {
    "area": "大区",
    "cancer": "肿瘤类型",
    "product_type": "产品",
    "department": "科室",
    "sample_type": "样本方式",
}


class DataProcessor:
    def __init__(self, file_path=None, dataframe=None):
        self.file_path = file_path
        self.dataframe = dataframe

    # def sale_category(self):
    #     """
    #     calculate sale amount according categories
    #     :return: dataframe
    #     """
    #     result = {}
    #     for key in category_dict.keys():
    #         result[key] = pd.pivot_table(self.df, index=[key], values=['price'], aggfunc=np.sum)
    #     return result

    def one_dimension(self, index, value, aggfunc=np.sum):
        if not index:
            raise ValueError("Need index.")
        return pd.pivot_table(self.dataframe, index=index, values=value, aggfunc=aggfunc)


class Graph:
    def __init__(self, nrows=1, ncols=1, savefig_path=None, title=None):
        self.fig, self.ax_list = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols*5, nrows*5))
        self.savefig_path = savefig_path
        self.title = title

    def callback(self, graph_type, *args):
        method = getattr(self, graph_type, None)
        if callable(method):
            method(*args)
        plt.savefig(self.savefig_path)

    def bar(self, df, ax, fold=None, category=None):
        if fold:
            df = df/fold
        x = np.arange(len(df))
        x_label = df.index.values.tolist()
        y = df.iloc[:, 0].values.tolist()
        rects = ax.bar(x, y)
        ax.set_xticks(x)
        ax.set_xticklabels(x_label, rotation=-45, ha='left')
        if fold:
            ylabel = "销量（x{}）".format(str(fold))
        else:
            ylabel = "销量"
        ax.set_ylabel(ylabel)
        title = "销量分布（按{}）".format(category[df.index.name])
        ax.set_title(title)
        self.autolabel(ax, rects)
        return rects

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


class Chandler:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def index_graph(self, category):
        ncols = 3
        nrows = int(np.ceil(len(category)/ncols))
        graph = Graph(nrows=nrows, ncols=ncols, savefig_path="/home/murphy/sale/static/images/stat.png", title="test")
        data_processor = DataProcessor(dataframe=self.dataframe)
        df_list = [data_processor.one_dimension(index=i, value='price', aggfunc=np.sum) for i in category]
        for i in range(len(df_list), ncols*nrows):
            df_list.insert(i, None)
        mat = np.array(df_list).reshape(nrows, ncols)
        for i in range(nrows):
            for j in range(ncols):
                d = mat[i][j]
                ax = graph.ax_list[i][j]
                if "None" not in str(type(d)):
                    graph.callback("bar", d, ax, 1000, category_dict)

# class Chandler(DataProcessor, Plot):
#     def __init__(self, file_path=None, df=None):
#         DataProcessor.__init__(self, file_path=file_path, df=df)
#         Plot.__init__(self, savefig_path="/home/murphy/django/static/images/stat.png")
#
#     def for_index_view(self):
#         input_df = self.one_dimension(index='department', value='price')
#         self.callback("bar", input_df)
#         return
