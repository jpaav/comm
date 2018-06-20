from django import template
from django.contrib.auth.models import User

from patientlog.models import Tag, Resident

register = template.Library()


@register.tag
def tag_name_from_id(ids):
	full_string = ""
	for tag_id in str.split(ids, "_"):
		if tag_id == "":
			continue
		try:
			full_string += Tag.objects.get(pk=tag_id).title + ", "
		except Tag.DoesNotExist:
			return "No Such Tag"
	# This expression removes the last ", " from the string
	return full_string[:-2]


@register.tag
def resident_name_from_id(ids):
	full_string = ""
	for resident_id in str.split(ids, "_"):
		if resident_id == "":
			continue
		try:
			full_string += Resident.objects.get(pk=resident_id).name + ", "
		except Resident.DoesNotExist:
			return "No Such Resident"
	# This expression removes the last ", " from the string
	return full_string[:-2]


@register.tag
def logger_name_from_id(ids):
	full_string = ""
	for user_id in str.split(ids, "_"):
		if user_id == "":
			continue
		try:
			full_string += User.objects.get(pk=user_id).get_full_name() + ", "
		except User.DoesNotExist:
			return "No Such User"
	# This expression removes the last ", " from the string
	return full_string[:-2]


register.filter('tag_name_from_id', tag_name_from_id)
register.filter('resident_name_from_id', resident_name_from_id)
register.filter('logger_name_from_id', logger_name_from_id)