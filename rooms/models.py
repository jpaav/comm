from django.contrib.auth.models import User
from django.db import models

from orgs.models import Org


class Room(models.Model):
	objects = models.Manager()
	members = models.ForeignKey(
		User
	)
	org = models.ForeignKey(
		Org,
		null=True
	)