from django.apps import apps
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
from matplotlib.ticker import MaxNLocator
from collections import namedtuple
import scipy.stats as stats


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

    def read_file(self):
        return pd.read_excel(self.file_path, sheet_name='Sheet1')

    def sale_category(self):
        """
        calculate sale amount according categories
        :return: dataframe
        """
        result = {}
        for key in category_dict.keys():
            result[key] = pd.pivot_table(self.df, index=[key], values=['price'], aggfunc=np.sum)
        return result


class Plot:
    def __init__(self, ax, data, *args):
        self.ax = ax
        self.data = data
        self.args = args


class Chandler(DataProcessor, Plot):
    def __callback(self, process, *args):
        method = getattr(self, process, None)
        if callable(method):
            method(*args)

    def test(self):
        self.sale_category()
