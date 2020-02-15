from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import View, TemplateView, DetailView
from .forms import UploadFileForm
from .models import SaleData


# GLOBAL CONSTANTS
EMPLOYEE = {}


class IndexView(View):
    def get(self, request):
        return render(request, 'analysis/index.html', {})


class ProjectView(View):
    def get(self, request):
        pass


class UploadSaleDataView(View):

    def get(self, request):
        form = UploadFileForm()
        return render(request, 'analysis/upload_sale_data.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('template_file')
            for f in files:
                print(f)
        return HttpResponse("OK")
