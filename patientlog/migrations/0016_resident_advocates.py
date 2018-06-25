# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-25 11:35
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('patientlog', '0015_auto_20180619_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='resident',
            name='advocates',
            field=models.ManyToManyField(blank=True, null=True, related_name='advocates', to=settings.AUTH_USER_MODEL),
        ),
    ]
