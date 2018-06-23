# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-23 14:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('task', '0006_auto_20180623_1513'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchedulerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interval', models.FloatField()),
                ('last_added', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='TaskPatternModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('tag', models.CharField(max_length=10)),
                ('status', models.IntegerField(choices=[(0, 'UNDONE'), (1, 'PROCESS'), (2, 'DONE')], default=0)),
                ('priority', models.IntegerField(choices=[(0, 'LOW'), (1, 'MEDIUM'), (2, 'HIGH')])),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='task.TaskPatternModel')),
            ],
        ),
    ]
