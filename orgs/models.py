from django.contrib.auth.models import User
from django.db import models


class Org(models.Model):
	def __str__(self):
		return 'Org: ' + self.name
	objects = models.Manager()
	name = models.CharField(max_length=50, null=True)
	description = models.CharField(max_length=1000, null=True, blank=True)
	location = models.CharField(max_length=100, null=True, blank=True)
	owner = models.ForeignKey(
		User,
		null=True,
		related_name='owner',
	)
	# TODO Check if this should be "CASCADE"
	members = models.ManyToManyField(
		User,
		related_name='members',
		blank=True
	)
	unapproved = models.ManyToManyField(
		User,
		related_name='unapproved',
		blank=True
	)
