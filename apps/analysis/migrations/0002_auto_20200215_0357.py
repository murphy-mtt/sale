# Generated by Django 2.0 on 2020-02-15 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='order_type',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='订单类型'),
        ),
        migrations.AddField(
            model_name='orders',
            name='patient',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='受检者'),
        ),
        migrations.AddField(
            model_name='orders',
            name='price',
            field=models.FloatField(blank=True, null=True, verbose_name='订单价格'),
        ),
        migrations.AddField(
            model_name='orders',
            name='product_type',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='产品名称'),
        ),
        migrations.AddField(
            model_name='orders',
            name='quotation',
            field=models.FloatField(blank=True, null=True, verbose_name='产品价格'),
        ),
        migrations.AddField(
            model_name='orders',
            name='sample_type',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='样本方式'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='create_date',
            field=models.DateTimeField(verbose_name='创建订单时间'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_id',
            field=models.IntegerField(verbose_name='送检单号'),
        ),
    ]
