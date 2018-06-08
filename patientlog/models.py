from django.contrib.auth.models import User
from django.db import models

from orgs.models import Org


class Tag(models.Model):
	objects = models.Manager()
	color = models.CharField(max_length=6)
	title = models.CharField(max_length=100)
	org = models.ForeignKey(
		Org,
		null=False
	)


class Log(models.Model):
	objects = models.Manager()
	org = models.ForeignKey(
		Org,
		null=True,
		related_name='org',
	)
	name = models.CharField(max_length=50, null=True)
	description = models.CharField(max_length=1000, null=True)
	location = models.CharField(max_length=100, null=True)


class Entry(models.Model):
	objects = models.Manager()
	participants = models.ForeignKey(
		User,
		null=True,
		related_name='participants'
	)
	logger = models.ForeignKey(
		User,
		null=True,
		related_name='logger'
	)
	message = models.CharField(max_length=1000)
	tags = models.ForeignKey(
		Tag,
		null=True,
		related_name='tags'
	)
	log = models.ForeignKey(
		Log,
		null=True,
		related_name='log',
	)
