from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import View, TemplateView, DetailView
from django.apps import apps

from django_pandas.io import read_frame
import numpy as np

from .forms import UploadFileForm
from .models import SaleData, Orders
from utils.data_process import DataProcessor, Chandler

# GLOBAL CONSTANTS
EMPLOYEE = {}
qs = Orders.objects.all()
df = read_frame(qs)


class IndexView(View):
    def get(self, request):
        monica = Chandler(df=df)
        a = monica.for_index_view()
        return render(request, 'analysis/index.html', {})


class ProjectView(View):
    def get(self, request):
        pass


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
