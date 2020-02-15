from django.db import models
from django.forms import ModelForm

# Create your models here.


class Orders(models.Model):
    detecting_id = models.CharField(max_length=20, verbose_name="送检单号", blank=True, null=True)
    detecting_id_bk = models.CharField(max_length=20, verbose_name="单号", blank=True, null=True)
    create_date = models.DateTimeField(verbose_name="创建订单时间", blank=True, null=True)
    patient = models.CharField(max_length=20, verbose_name="受检者", blank=True, null=True)
    patient_condition = models.CharField(max_length=200, verbose_name="患者情况", blank=True, null=True)
    order_type = models.CharField(max_length=20, verbose_name="订单类型", blank=True, null=True)
    product_type = models.CharField(max_length=50, verbose_name="产品名称", blank=True, null=True)
    sample_type = models.CharField(max_length=20, verbose_name="样本方式", blank=True, null=True)
    blood_type = models.CharField(max_length=20, verbose_name="血液类型", blank=True, null=True)
    quotation = models.FloatField(verbose_name="产品价格", blank=True, null=True)
    price = models.FloatField(verbose_name="订单价格", blank=True, null=True)
    price_of_consulting = models.FloatField(verbose_name="报告解读费", blank=True, null=True)
    collection = models.FloatField(verbose_name="收款金额", blank=True, null=True)
    refund = models.FloatField(verbose_name="退款金额", blank=True, null=True)
    collection_date = models.DateTimeField(verbose_name='收款日期', blank=True, null=True)
    pay_method = models.CharField(max_length=100, verbose_name="支付方式", blank=True, null=True)
    comment = models.CharField(max_length=500, verbose_name="备注信息", blank=True, null=True)
    area = models.CharField(max_length=10, verbose_name="大区", blank=True, null=True)
    area_manager = models.CharField(max_length=10, verbose_name="大区经理", blank=True, null=True)
    region = models.CharField(max_length=20, verbose_name="地区", blank=True, null=True)
    region_manager = models.CharField(max_length=20, verbose_name="地区经理", blank=True, null=True)
    sale_person = models.CharField(max_length=20, verbose_name="销售姓名", blank=True, null=True)
    hospital_region = models.CharField(max_length=30, verbose_name="医院地区", blank=True, null=True)
    hospital = models.CharField(max_length=50, verbose_name="医院", blank=True, null=True)
    doctor = models.CharField(max_length=50, verbose_name="送检医生", blank=True, null=True)
    department = models.CharField(max_length=20, verbose_name="科室", blank=True, null=True)
    cancer = models.CharField(max_length=20, verbose_name="癌种", blank=True, null=True)
    comes_from = models.CharField(max_length=30, verbose_name="来源机构", blank=True, null=True)
    project_id = models.CharField(max_length=20, verbose_name="项目编号", blank=True, null=True)
    project_name = models.CharField(max_length=40, verbose_name="项目名称", blank=True, null=True)
    project_PI = models.CharField(max_length=20, verbose_name="合作pi", blank=True, null=True)
    order_id = models.CharField(max_length=30, verbose_name="订单编号", blank=True, null=True)
    express_fee = models.FloatField(verbose_name="快递费用", blank=True, null=True)
    payment_id = models.CharField(max_length=30, verbose_name="支付单号", blank=True, null=True)
    sample_status = models.CharField(max_length=20, verbose_name="样本状态", blank=True, null=True)
    order_checking_status = models.CharField(max_length=16, verbose_name="订单审核", blank=True, null=True)
    dry_ice_number = models.FloatField(verbose_name="干冰数量", blank=True, null=True)
    dry_ice_fee = models.FloatField(verbose_name="干冰费用", blank=True, null=True)
    express_order1 = models.CharField(max_length=30, verbose_name="邮寄单号1", blank=True, null=True)
    express_date1 = models.DateField(verbose_name="邮寄日期1", blank=True, null=True)
    express_company1 = models.CharField(max_length=30, verbose_name="快递公司1", blank=True, null=True)
    express_type1 = models.CharField(max_length=200, verbose_name="邮寄类型1", blank=True, null=True)
    express_order2 = models.CharField(max_length=30, verbose_name="邮寄单号2", blank=True, null=True)
    express_date2 = models.DateField(verbose_name="邮寄日期2", blank=True, null=True)
    express_company2 = models.CharField(max_length=30, verbose_name="快递公司2", blank=True, null=True)
    express_type2 = models.CharField(max_length=200, verbose_name="邮寄类型2", blank=True, null=True)
    in_storage_time = models.DateField(verbose_name='入库时间', blank=True, null=True)
    platform = models.CharField(max_length=40, verbose_name="平台", blank=True, null=True)

    class Meta:
        unique_together = (('detecting_id', 'create_date'),)

    def __str__(self):
        return self.detecting_id


def template_file_path(instance, filename):
    return "uploads/{}/templates/{}".format(instance.query_user.id, filename)


class SaleData(models.Model):
    template_file = models.FileField(upload_to=template_file_path, verbose_name="销售数据文件")
    upload_time = models.DateTimeField(auto_now=True, verbose_name="上传时间", help_text="用户何时上传此文件", null=True)
