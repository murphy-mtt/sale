from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):
    USER_TYPE_CHOICE = (
        ("PRODUCT_MANAGER", "产品经理"),
        ("REGIONAL_MANAGER", "区域经理"),
        ("MARKET", "市场支持"),
        ("SALE", "销售"),
    )
    GENDER = (
        ("male", "男"),
        ("female", "女")
    )
    
    nick_name = models.CharField(max_length=50, verbose_name="姓名", default="", blank=True, null=True)
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, default="female", verbose_name="性别")
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICE, default="OTHERS")
    area = models.CharField(max_length=100, verbose_name="大区", default="", blank=True, null=True)
    region = models.CharField(max_length=100, verbose_name="地区", default="", blank=True, null=True)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


