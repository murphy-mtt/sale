from . import views
from django.urls import path

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('upload_sale_data', views.UploadSaleDataView.as_view(), name='upload_sale_data'),
    path('my_area/<int:user_id>', views.AreaSaleView.as_view(), name='my_area'),
    path('saleman/<str:saleman>', views.SalePersonView.as_view(), name="saleman"),
    path('regionsale/<str:region>', views.RegionSaleView.as_view(), name='regionsale'),
    path('downloaddata', views.DownloadDataView.as_view(), name='downloaddata'),
]
