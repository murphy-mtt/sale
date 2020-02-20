from django.contrib import admin
from .models import SaleData, Orders

# Register your models here.

admin.site.site_title = "Haplox产品市场部"
admin.site.site_header = "Haplox产品市场部"
admin.site.index_title = "Haplox产品市场部"


@admin.register(Orders)
class UserQueryAdmin(admin.ModelAdmin):
    list_display = ['detecting_id', 'cancer', 'area', 'region', 'area_manager', 'region_manager', 'sale_person', 'hospital', 'department', 'doctor', 'product_type']
    list_filter = ['cancer', 'area', 'region', 'area_manager', 'region_manager', 'sale_person',
                    'hospital', 'department', 'doctor', 'product_type', 'create_date']
    search_fields = ['detecting_id', 'cancer', 'area', 'region', 'area_manager', 'region_manager', 'sale_person', 'hospital', 'department', 'doctor', 'product_type']
