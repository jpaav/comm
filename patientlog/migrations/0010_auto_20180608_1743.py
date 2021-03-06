# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-08 21:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patientlog', '0009_auto_20180608_1722'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='participants',
        ),
        migrations.AddField(
            model_name='entry',
            name='residents',
            field=models.ManyToManyField(null=True, related_name='residents', to='patientlog.Resident'),
        ),
        migrations.RemoveField(
            model_name='entry',
            name='tags',
        ),
        migrations.AddField(
            model_name='entry',
            name='tags',
            field=models.ManyToManyField(null=True, related_name='tags', to='patientlog.Tag'),
        ),
    ]
