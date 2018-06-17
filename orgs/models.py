from django.contrib.auth.models import User
from django.db import models


class Org(models.Model):
	objects = models.Manager()
	name = models.CharField(max_length=50, null=True)
	description = models.CharField(max_length=1000, null=True)
	location = models.CharField(max_length=100, null=True)
	owner = models.ForeignKey(
		User,
		null=True,
		related_name='owner',
	)
	# TODO Check if this should be "CASCADE"
	members = models.ManyToManyField(
		User,
		related_name='members',
	)
	unapproved = models.ManyToManyField(
		User,
	)
