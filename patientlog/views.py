import math
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.db.models.functions import datetime
from django.shortcuts import render, redirect

from patientlog.forms import CreateEntryForm
from patientlog.models import Log, Entry, Resident


def get_form_kwargs(self):
	kwargs = super(self).get_form_kwargs()
	kwargs.update({'log': Log()})
	return kwargs


def log(request, log_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	try:
		log = Log.objects.get(pk=log_id)
	except ObjectDoesNotExist:
		return render(request, 'patientlogs/object_does_not_exist.html', {'obj_type': 'log'})
	# Make sure the user is a member and can view this log
	if request.user not in log.org.members.all():
		return render(request, 'accounts/not_authorized.html')
	# Get variables from URL that alter view
	# Second argument is default value
	sort = request.GET.get('sort', 'newest')
	try:
		offset = int(request.GET.get('offset', '0'))
	# If the user supplies some bogus offset it will be caught here and changed to zero
	except ValueError:
		return redirect('/logs/' + str(log_id) + '/?sort=' + str(sort) + '&offset=0')
	count = Entry.objects.filter(log=log).count()
	# Returns the largest multiple of 100 less than count if the offset is too large or is -1
	# The negative -1 option is so that the template can go to the end without knowing the count
	if offset > count or offset == -1:
		offset = int(math.floor(count / 100.0)) * 100
		return redirect('/logs/' + str(log_id) + '/?sort=' + str(sort) + '&offset=' + str(offset))
	# Returns the largest multiple of 100 less than offset
	# Used to make sure offsets are multiples of 100 (ie 134 becomes 100 and 202 becomes 200)
	if not offset % 100 == 0:
		offset = int(math.floor(offset / 100.0)) * 100
		return redirect('/logs/' + str(log_id) + '/?sort=' + str(sort) + '&offset=' + str(offset))
	# Sorts by the newest timestamp in the entries
	if sort == 'newest':
		entries = Entry.objects.filter(log=log).order_by('-timestamp')[offset:100]
	# Sorts by the oldest timestamp in the entries
	elif sort == 'oldest':
		entries = Entry.objects.filter(log=log).order_by('timestamp')[offset:100]
	# If the user supplies some bogus filter it will be caught here and changed to newest
	else:
		return redirect('/logs/' + str(log_id) + '/?sort=newest&offset=' + str(offset))
	return render(request, 'patientlogs/log.html', {'log': log, 'entries': entries, 'sort': sort, 'offset': offset})


def log_detail(request, log_id, entry_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	try:
		log = Log.objects.get(pk=log_id)
	except ObjectDoesNotExist:
		return render(request, 'patientlogs/object_does_not_exist.html', {'obj_type': 'log'})
	# Make sure the user is a member and can view this log
	if request.user not in log.org.members.all():
		return render(request, 'accounts/not_authorized.html')
	# Get variables from URL that alter view
	# Second argument is default value
	sort = request.GET.get('sort', 'newest')
	try:
		offset = int(request.GET.get('offset', '0'))
	# If the user supplies some bogus offset it will be caught here and changed to zero
	except ValueError:
		return redirect('/logs/' + str(log_id) + '/?sort=' + str(sort) + '&offset=0')
	count = Entry.objects.filter(log=log).count()
	# Returns the largest multiple of 100 less than count if the offset is too large or is -1
	# The negative -1 option is so that the template can go to the end without knowing the count
	if offset > count or offset == -1:
		offset = int(math.floor(count / 100.0)) * 100
		return redirect('/logs/' + str(log_id) + '/?sort=' + str(sort) + '&offset=' + str(offset))
	# Returns the largest multiple of 100 less than offset
	# Used to make sure offsets are multiples of 100 (ie 134 becomes 100 and 202 becomes 200)
	if not offset % 100 == 0:
		offset = int(math.floor(offset / 100.0)) * 100
		return redirect('/logs/' + str(log_id) + '/?sort=' + str(sort) + '&offset=' + str(offset))
	# Sorts by the newest timestamp in the entries
	if sort == 'newest':
		entries = Entry.objects.filter(log=log).order_by('-timestamp')[offset:100]
	# Sorts by the oldest timestamp in the entries
	elif sort == 'oldest':
		entries = Entry.objects.filter(log=log).order_by('timestamp')[offset:100]
	# If the user supplies some bogus filter it will be caught here and changed to newest
	else:
		return redirect('/logs/' + str(log_id) + '/?sort=newest&offset=' + str(offset))
	# Get the detail object based on the entry_id
	try:
		detail = Entry.objects.get(pk=entry_id)
	except ObjectDoesNotExist:
		return render(request, 'patientlogs/object_does_not_exist.html', {'obj_type': 'entry'})
	return render(request, 'patientlogs/log.html', {'log': log, 'entries': entries, 'detail': detail, 'sort': sort,
													'offset': offset})


def new_entry(request, log_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	try:
		log = Log.objects.get(pk=log_id)
	except ObjectDoesNotExist:
		return render(request, 'patientlogs/object_does_not_exist.html', {'obj_type': 'log'})
	# Make sure the user is a member and can view this log
	if request.user not in log.org.members.all():
		return render(request, 'accounts/not_authorized.html')
	# Render the form if GET otherwise save the info from POST
	if request.method == 'GET':
		form = CreateEntryForm(log=log)
	else:
		form = CreateEntryForm(request.POST, log=log)
		if form.is_valid():
			entry = form.save(commit=False)
			entry.logger = request.user
			entry.timestamp = datetime.datetime.now()
			entry.save()
			# Because this is many to many you have to add them after saving the inital object
			for resident in form.clean_residents():
				entry.residents.add(resident)
			for tag in form.clean_tags():
				entry.tags.add(tag)
			return redirect('/logs/' + str(log_id))

	return render(request, 'patientlogs/new_entry.html', {'log': log, 'form': form})
