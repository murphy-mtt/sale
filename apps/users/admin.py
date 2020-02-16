from django.contrib import admin
from .models import UserProfile

# Register your models here.


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_staff', 'is_active']
