# Generated by Django 2.0 on 2020-02-15 11:31

import analysis.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0002_saledata'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='detecting_id_bk',
            field=models.IntegerField(blank=True, null=True, verbose_name='单号'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='price_of_consulting',
            field=models.FloatField(blank=True, null=True, verbose_name='报告解读费'),
        ),
        migrations.AlterField(
            model_name='saledata',
            name='template_file',
            field=models.FileField(upload_to=analysis.models.template_file_path, verbose_name='销售数据文件'),
        ),
    ]
