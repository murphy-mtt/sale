from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import View, TemplateView, DetailView


class IndexView(View):
    def get(self, request):
        return render(request, 'analysis/index.html', {})


class ProjectView(View):
    def get(self, request):
        pass
