# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-21 22:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20180618_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='settings',
            field=models.CharField(blank=True, default='simple_ui=true;', max_length=1000),
        ),
    ]
