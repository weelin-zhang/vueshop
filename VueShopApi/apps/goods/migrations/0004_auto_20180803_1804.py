# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-03 18:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20180803_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodscategorybrand',
            name='image',
            field=models.ImageField(max_length=200, upload_to='brand/'),
        ),
        migrations.AlterField(
            model_name='goodsimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='goods/images/', verbose_name='图片'),
        ),
    ]
