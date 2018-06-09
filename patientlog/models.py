from django.contrib.auth.models import User
from django.db import models

from orgs.models import Org


class Tag(models.Model):
	objects = models.Manager()
	color = models.CharField(max_length=6)
	title = models.CharField(max_length=100)
	org = models.ForeignKey(
		Org,
		null=False,
		related_name='tag_org'
	)


class Resident(models.Model):
	objects = models.Manager()
	name = models.CharField(max_length=50)
	org = models.ForeignKey(
		Org,
		null=True,
		related_name='resident_org'
	)


class Log(models.Model):
	objects = models.Manager()
	org = models.ForeignKey(
		Org,
		null=True,
		related_name='log_org',
	)
	name = models.CharField(max_length=50, null=True)
	description = models.CharField(max_length=1000, null=True)
	location = models.CharField(max_length=100, null=True)


class Entry(models.Model):
	objects = models.Manager()
	residents = models.ManyToManyField(
		Resident,
		null=True,
		related_name='residents',

	)
	logger = models.ForeignKey(
		User,
		null=True,
		related_name='logger'
	)
	message = models.CharField(max_length=1000)
	tags = models.ManyToManyField(
		Tag,
		null=True,
		related_name='tags'
	)
	log = models.ForeignKey(
		Log,
		null=True,
		related_name='log',
	)
	timestamp = models.DateTimeField(null=True)
