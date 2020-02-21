from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import View, TemplateView, DetailView
from django.apps import apps

from django_pandas.io import read_frame
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.patches import ConnectionPatch

from .forms import UploadFileForm
from .models import SaleData, Orders
from utils.data_process import DataProcessor, Chandler
from users.models import UserProfile

# GLOBAL CONSTANTS
EMPLOYEE = {}
qs = Orders.objects.all()
df = read_frame(qs)


def getmodelfield(appname, modelname, exclude):
    """
    获取model的verbose_name和name的字段
    """
    modelobj = apps.get_model(appname, modelname)
    filed = modelobj._meta.fields
    fielddic = {}
    params = [f for f in filed if f.name not in exclude]
    for i in params:
        fielddic[i.name] = i.verbose_name
    return fielddic


class IndexView(View):
    def get(self, request):
        category_dict = {
            "area": "大区",
            "cancer": "肿瘤类型",
            "department": "科室",
            "sample_type": "样本方式",
            "order_type": "订单类型",
            "product_type": "产品",
        }
        monica = Chandler(dataframe=df)
        a = monica.index_graph(category_dict)
        areas = list(set(df.area.values.tolist()))
        return render(request, 'analysis/index.html', {
            "areas": areas,
        })


class UploadSaleDataView(View):
    """
    上传数据文件，保存如数据库，同时保存文件
    """
    @staticmethod
    def getmodelfield(appname, modelname, exclude):
        """
        获取model的verbose_name和name的字段
        """
        modelobj = apps.get_model(appname, modelname)
        filed = modelobj._meta.fields
        fielddic = {}
        params = [f for f in filed if f.name not in exclude]
        for i in params:
            fielddic[i.name] = i.verbose_name
        return fielddic

    def get(self, request):
        form = UploadFileForm()
        return render(request, 'analysis/upload_sale_data.html', {
            'form': form
        })

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        cs = self.getmodelfield('analysis', 'Orders', ['id'])

        if form.is_valid():
            files = request.FILES.getlist('template_file')
            for f in files:
                file_path = f.temporary_file_path()
                df = pd.read_excel(file_path, sheet_name='Sheet1')
                for i in range(len(df.index)):
                    row = df.iloc[i, :]
                    order = Orders()
                    for j in df.columns:
                        try:
                            value = getattr(row, j)
                            key = list(cs.keys())[list(cs.values()).index(j)]
                            setattr(order, key, value)
                        except ValueError:
                            pass
                    try:
                        order.save()
                    except Exception as e:
                        pass
        return HttpResponseRedirect("../analysis")


class AreaSaleView(View):
    def get(self, request, user_id):
        user = UserProfile.objects.get(id=user_id)
        my_area = user.area
        my_df = df.loc[df.area.isin([my_area]), :]
        cs = getmodelfield('analysis', 'Orders', [])
        my_df_desc = my_df.describe().applymap("{0:.02f}".format)
        my_df_desc.columns = [cs[key] for key in my_df_desc.columns]
        my_df_index = my_df_desc.index.values.tolist()
        sale_list = list(set(df.sale_person.values.tolist()))
        region_list = list(set(df.region.values.tolist()))
        return render(request, 'analysis/myarea.html', {
            "my_area": my_area,
            "my_df_desc": my_df_desc.to_html(),
            "my_df_index": my_df_index,
            "sale_list": sale_list,
            "region_list": region_list,
        })


class SalePersonView(View):
    def get(self, request, saleman):
        sale_df = df.loc[df.sale_person.isin([saleman]), :]
        sale_df.doctor = sale_df.doctor.fillna('未填写')
        category_dict = {
            "cancer": "肿瘤类型",
            "department": "科室",
            "product_type": "产品",
            "doctor": "送检医生",
        }
        graph1 = Chandler(dataframe=sale_df)
        graph1.sale_bar_graph(category=category_dict)
        graph1.sale_ranking_graph(df, saleman)
        return render(request, 'analysis/saleman.html', {})


class RegionSaleView(View):
    def get(self, request, region):
        df_bp = pd.pivot_table(df, index=['region', 'sale_person'], values=['price'], aggfunc=np.sum).fillna(0)
        graph = Chandler(df)
        graph.region_distribution(region=region)
        # counts1 = []
        # lables1 = df_bp.index.levels[0].values.tolist()
        # region_index = lables1.index(region)
        # item = lables1.pop(region_index)
        # lables1.insert(0, item)
        # for i in lables1:
        #     counts1.append(df_bp.loc[i].sum()[0])
        # counts1 = np.array(counts1) / float(np.array(counts1).sum())
        # count2 = df_bp.loc[region].values / float(df_bp.loc[region].values.sum())
        # labels2 = df_bp.loc[region].index.tolist()
        #
        # fig = plt.figure(figsize=(9, 5.0625))
        # ax1 = fig.add_subplot(121)
        # ax2 = fig.add_subplot(122)
        # fig.subplots_adjust(wspace=0)
        #
        # # pie chart parameters
        # ratios = counts1
        # labels = lables1
        # # rotate so that first wedge is split by the x-axis
        # angle = -180 * ratios[0]
        # ax1.pie(ratios, autopct='%1.1f%%', startangle=angle,
        #         labels=labels)
        #
        # # bar chart parameters
        #
        # xpos = 0
        # bottom = 0
        # ratios = count2
        # width = .2
        #
        # for j in range(len(ratios)):
        #     height = ratios[j]
        #     ax2.bar(xpos, height, width, bottom=bottom)
        #     ypos = bottom + ax2.patches[j].get_height() / 2
        #     bottom += height
        #     ax2.text(xpos, ypos, "%d%%" % (ax2.patches[j].get_height() * 100),
        #              ha='center')
        #
        # ax2.set_title('Age of approvers')
        # ax2.legend(labels2)
        # ax2.axis('off')
        # ax2.set_xlim(- 2.5 * width, 2.5 * width)
        #
        # # use ConnectionPatch to draw lines between the two plots
        # # get the wedge data
        # theta1, theta2 = ax1.patches[0].theta1, ax1.patches[0].theta2
        # center, r = ax1.patches[0].center, ax1.patches[0].r
        # bar_height = sum([item.get_height() for item in ax2.patches])
        #
        # # draw top connecting line
        # x = r * np.cos(np.pi / 180 * theta2) + center[0]
        # y = np.sin(np.pi / 180 * theta2) + center[1]
        # con = ConnectionPatch(xyA=(- width / 2, bar_height), xyB=(x, y),
        #                       coordsA="data", coordsB="data", axesA=ax2, axesB=ax1)
        # con.set_color([0, 0, 0])
        # con.set_linewidth(4)
        # ax2.add_artist(con)
        #
        # # draw bottom connecting line
        # x = r * np.cos(np.pi / 180 * theta1) + center[0]
        # y = np.sin(np.pi / 180 * theta1) + center[1]
        # con = ConnectionPatch(xyA=(- width / 2, 0), xyB=(x, y), coordsA="data",
        #                       coordsB="data", axesA=ax2, axesB=ax1)
        # con.set_color([0, 0, 0])
        # ax2.add_artist(con)
        # con.set_linewidth(4)
        # plt.savefig("/home/murphy/sale/static/images/region_distribution.png")
        return render(request, 'analysis/regionsale.html', {})


class RegionPersonView(View):
    def get(self, request, user_id):
        user = UserProfile.objects.get(id=user_id)
        my_area = user.area
        my_df = df.loc[df.area.isin([my_area]), :]
        monica = Chandler(dataframe=my_df)
        return render(request, 'analysis/saleman.html', {})
