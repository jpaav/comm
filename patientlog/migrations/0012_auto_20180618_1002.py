# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-18 14:02
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patientlog', '0011_auto_20180613_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='logger',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='logger', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='entry',
            name='message',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='entry',
            name='residents',
            field=models.ManyToManyField(blank=True, related_name='residents', to='patientlog.Resident'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='patientlog.Tag'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='timestamp',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='log',
            name='location',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
