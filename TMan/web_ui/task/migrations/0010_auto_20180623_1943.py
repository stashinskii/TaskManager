# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-23 16:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0009_auto_20180623_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.IntegerField(choices=[(0, 'LOW'), (1, 'MEDIUM'), (2, 'HIGH')], default=2),
        ),
    ]