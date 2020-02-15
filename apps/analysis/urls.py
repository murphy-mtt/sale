from . import views
from django.urls import path

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('upload_sale_data', views.UploadSaleDataView.as_view(), name='upload_sale_data'),
]
