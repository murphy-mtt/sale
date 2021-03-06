import os
import numpy as np
import pandas as pd
import xlsxwriter
import tempfile
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch
from io import BytesIO


from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import View, TemplateView, DetailView
from django.apps import apps
from django_pandas.io import read_frame

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
        monica = Chandler(dataframe=df, username=request.user.username)
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


class DownloadDataView(View):
    def get(self, request):
        user = UserProfile.objects.get(username=request.user)
        my_area = user.area
        my_df = df.loc[df.area.isin([my_area]), :]
        my_df['create_date'] = my_df['create_date'].apply(lambda x: x.strftime('%Y-%m-%d'))
        cs = getmodelfield('analysis', 'Orders', [])
        my_df.columns = [cs[key] for key in my_df.columns]
        with tempfile.TemporaryDirectory() as tmpdirname:
            os.chdir(tmpdirname)
            x_io = BytesIO()
            workbook = xlsxwriter.Workbook(x_io, {'remove_timezone': True})
            worksheet1 = workbook.add_worksheet('Sheet1')
            row, col = 0, 0
            for c in my_df.columns:
                worksheet1.write(row, col, c)
                col += 1
            row, col = 1, 0
            for i in range(len(my_df)):
                for j in range(len(my_df.columns)):
                    item = my_df.iloc[i, j]
                    worksheet1.write(row, col, str(item))
                    col += 1
                row += 1
                col = 0
            workbook.close()
            response = HttpResponse()
            response["Content-Type"] = "application/octet-stream"
            response["Content-Disposition"] = 'attachment; filename="sale.xlsx"'
            response.write(x_io.getvalue())
            return response


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
        graph = Chandler(my_df, request.user.username)
        graph.region_stacked_graph()
        region_sale_performance = pd.pivot_table(df, index=['region', 'sale_person'], values=['price'], aggfunc=np.sum)
        rsp = Chandler(region_sale_performance, request.user.username)
        rsp.region_sale_performance()
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
        graph1 = Chandler(dataframe=sale_df, username=request.user.username)
        graph1.sale_bar_graph(category=category_dict)
        graph1.sale_ranking_graph(df, saleman)
        return render(request, 'analysis/saleman.html', {})


class RegionSaleView(View):
    def get(self, request, region):
        graph = Chandler(df, request.user.username)
        graph.region_distribution(region=region)
        return render(request, 'analysis/regionsale.html', {})


class RegionPersonView(View):
    def get(self, request, user_id):
        user = UserProfile.objects.get(id=user_id)
        my_area = user.area
        my_df = df.loc[df.area.isin([my_area]), :]
        monica = Chandler(dataframe=my_df, username=request.user.username)
        return render(request, 'analysis/saleman.html', {})
