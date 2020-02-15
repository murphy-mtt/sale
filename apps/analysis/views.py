from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import View, TemplateView, DetailView
from django.apps import apps

from .forms import UploadFileForm
from .models import SaleData, Orders
from utils.data_process import DataStorage


# GLOBAL CONSTANTS
EMPLOYEE = {}


class IndexView(View):
    def get(self, request):
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
                data_processor = DataStorage(file_path=f.temporary_file_path())
                df = data_processor.read_file()
                for i in range(len(df.index)):
                    row = df.iloc[i, :]
                    for j in df.columns:
                        order = Orders()
                        try:
                            value = getattr(row, j)
                            key = list(cs.keys())[list(cs.values()).index(j)]
                            print("{}: {}".format(key, value))
                            setattr(order, key, value)
                            order.save()
                        except ValueError:
                            pass
        return HttpResponse("OK")
