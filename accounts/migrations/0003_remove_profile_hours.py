# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-13 17:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20180607_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='hours',
        ),
    ]