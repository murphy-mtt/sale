from django.contrib import admin
from .models import SaleData, Orders

# Register your models here.


@admin.register(Orders)
class UserQueryAdmin(admin.ModelAdmin):
    list_display = ['detecting_id']
