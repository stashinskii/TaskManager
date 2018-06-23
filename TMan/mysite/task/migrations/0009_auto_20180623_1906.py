# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-23 16:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0008_auto_20180623_1756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskpatternmodel',
            name='author',
        ),
        migrations.RemoveField(
            model_name='taskpatternmodel',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='schedulermodel',
            name='task_pattern',
        ),
        migrations.AddField(
            model_name='schedulermodel',
            name='description',
            field=models.CharField(default=None, max_length=250),
        ),
        migrations.AddField(
            model_name='schedulermodel',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='schedulermodel',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='task.SchedulerModel'),
        ),
        migrations.AddField(
            model_name='schedulermodel',
            name='priority',
            field=models.IntegerField(choices=[(0, 'LOW'), (1, 'MEDIUM'), (2, 'HIGH')], default=2),
        ),
        migrations.AddField(
            model_name='schedulermodel',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='schedulermodel',
            name='status',
            field=models.IntegerField(choices=[(0, 'UNDONE'), (1, 'PROCESS'), (2, 'DONE')], default=0),
        ),
        migrations.AddField(
            model_name='schedulermodel',
            name='tag',
            field=models.CharField(default='None', max_length=10),
        ),
        migrations.AddField(
            model_name='schedulermodel',
            name='title',
            field=models.CharField(default='Empty title', max_length=50),
        ),
        migrations.DeleteModel(
            name='TaskPatternModel',
        ),
    ]
