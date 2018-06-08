# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-08 02:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patientlog', '0003_auto_20180607_2130'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='entries',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='patientlog.Entry'),
        ),
    ]
