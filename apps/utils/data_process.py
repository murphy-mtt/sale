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
    def __init__(self, file_path=None, df=None):
        self.file_path = file_path
        self.df = df

    def sale_category(self):
        """
        calculate sale amount according categories
        :return: dataframe
        """
        result = {}
        for key in category_dict.keys():
            result[key] = pd.pivot_table(self.df, index=[key], values=['price'], aggfunc=np.sum)
        return result

    def one_dimension(self, index, value, aggfunc=np.sum):
        if not index:
            raise ValueError("Need index.")
        return pd.pivot_table(self.df, index=index, values=value, aggfunc=aggfunc)


class Plot:
    def __init__(self, nrows=1, ncols=1, savefig_path=None):
        self.fig, self.ax = plt.subplots(nrows=nrows, ncols=ncols)
        self.savefig_path = savefig_path

    def callback(self, graph_type, *args):
        method = getattr(self, graph_type, None)
        if callable(method):
            method(*args)
        plt.savefig(self.savefig_path)

    def bar(self, df):
        x = np.arange(len(df))
        x_label = df.index.values.tolist()
        y = df.iloc[:, 0].values.tolist()
        rects = self.ax.bar(x, y)
        self.ax.set_xticks(x)
        self.ax.set_xticklabels(x_label, rotation=45, ha='right')
        self.autolabel(self.ax, rects)

    @staticmethod
    def autolabel(ax, rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')


class Chandler(DataProcessor, Plot):
    def __init__(self, file_path=None, df=None):
        DataProcessor.__init__(self, file_path=file_path, df=df)
        Plot.__init__(self, savefig_path="/home/murphy/django/static/images/stat.png")

    def for_index_view(self):
        input_df = self.one_dimension(index='department', value='price')
        self.callback("bar", input_df)
        return
