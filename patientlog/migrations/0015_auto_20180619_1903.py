# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-19 23:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patientlog', '0014_auto_20180618_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='timestamp_admitted',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='resident',
            name='timestamp_left',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]