from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

from orgs.models import Org


class Tag(models.Model):
	def __str__(self):
		return 'Tag: ' + self.title
	objects = models.Manager()
	color = models.CharField(max_length=6)
	title = models.CharField(max_length=100)
	org = models.ForeignKey(
		Org,
		null=False,
		related_name='tag_org'
	)


class Resident(models.Model):
	def __str__(self):
		return 'Resident: ' + self.name
	objects = models.Manager()
	name = models.CharField(max_length=50)
	org = models.ForeignKey(
		Org,
		null=True,
		related_name='resident_org'
	)
	room = models.CharField(max_length=20, blank=True)
	timestamp_admitted = models.DateTimeField(default=datetime.now, blank=True, null=True)
	timestamp_left = models.DateTimeField(default=datetime.now, blank=True, null=True)


class Log(models.Model):
	def __str__(self):
		return 'Log: ' + self.name
	objects = models.Manager()
	org = models.ForeignKey(
		Org,
		null=True,
		related_name='log_org',
	)
	name = models.CharField(max_length=50, null=True)
	description = models.CharField(max_length=1000, null=True, blank=True)
	location = models.CharField(max_length=100, null=True, blank=True)


class Entry(models.Model):
	def __str__(self):
		return 'Entry: ' + self.message[:500]
	objects = models.Manager()
	residents = models.ManyToManyField(
		Resident,
		related_name='residents',
		blank=True
	)
	logger = models.ForeignKey(
		User,
		null=True,
		related_name='logger',
		blank=True
	)
	message = models.CharField(max_length=1000, blank=True)
	tags = models.ManyToManyField(
		Tag,
		related_name='tags',
		blank=True
	)
	log = models.ForeignKey(
		Log,
		null=True,
		related_name='log',
	)
	timestamp = models.DateTimeField(null=True, default=datetime.now, blank=True)
