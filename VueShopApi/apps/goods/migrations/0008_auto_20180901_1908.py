# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-09-01 19:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0007_indexad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodscategorybrand',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='brands', to='goods.GoodsCategory', verbose_name='商品类目'),
        ),
        migrations.AlterField(
            model_name='goodscategorybrand',
            name='image',
            field=models.ImageField(max_length=200, upload_to='brands/'),
        ),
    ]
