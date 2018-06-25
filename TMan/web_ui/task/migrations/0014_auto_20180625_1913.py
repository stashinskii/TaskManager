# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-25 16:13
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0013_auto_20180625_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedulermodel',
            name='interval',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]