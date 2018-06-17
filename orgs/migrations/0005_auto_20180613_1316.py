# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-06-13 17:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orgs', '0004_auto_20180609_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='org',
            name='unapproved',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='org',
            name='members',
            field=models.ManyToManyField(related_name='members', to=settings.AUTH_USER_MODEL),
        ),
    ]
