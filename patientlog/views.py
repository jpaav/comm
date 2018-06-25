import math

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.db.models import QuerySet, Q, Count
from django.db.models.functions import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from comm import settings
from patientlog.forms import CreateEntryForm
from patientlog.models import Log, Entry, Resident, Tag


def get_form_kwargs(self):
	kwargs = super(self).get_form_kwargs()
	kwargs.update({'log': Log()})
	return kwargs


def log_resolve_offset(all_filter_str, offset, sort, log_id):
	count = Entry.objects.filter(log_id=log_id).count()
	# Returns the largest multiple of 100 less than count if the offset is too large or is -1
	# The negative -1 option is so that the template can go to the end without knowing the count
	if offset > count or offset == -1:
		offset = int(math.floor(count / 100.0)) * 100
		return redirect('/logs/' + str(log_id) + '/?sort=' + str(sort) + '&offset=' + str(offset) + "&" + all_filter_str)
	# Returns the largest multiple of 100 less than offset
	# Used to make sure offsets are multiples of 100 (ie 134 becomes 100 and 202 becomes 200)
	if not offset % 100 == 0:
		offset = int(math.floor(offset / 100.0)) * 100
		return redirect('/logs/' + str(log_id) + '/?sort=' + str(sort) + '&offset=' + str(offset) + "&" + all_filter_str)
	return None


def log_resolve_sort_and_filter(all_filter_str, res_filter, tag_filter, logger_filter, daterange_filter, sort, offset, log_id):
	# Separates each tag from the url and uses an OR filter to combine them with the overall query
	query = Q()
	for res in str.split(res_filter, "_"):
		if not res == "":
			query |= Q(residents=res)
	for tag in str.split(tag_filter, "_"):
		if not tag == "":
			query |= Q(tags=tag)
	for logger in str.split(logger_filter, "_"):
		if not logger == "":
			query |= Q(logger_id=logger)
	dates = str.split(daterange_filter, "_")
	if len(dates) == 2:
		try:
			start_date = datetime.datetime.strptime(dates[0], "%Y-%m-%d")
			end_date = datetime.datetime.strptime(dates[1], "%Y-%m-%d")
			query &= Q(timestamp__gte=start_date)
			query &= Q(timestamp__lte=end_date)
		except ValueError:
			pass

	# Filters by query, AND the correct log
	# Sorts by the timestamp in the entries
	# Removes duplicates
	# Cuts out 100 objects at the right index
	if sort == 'newest':
		return Entry.objects.filter(query, log_id=log_id).order_by('-timestamp').distinct()[offset:offset+100]
	elif sort == 'oldest':
		return Entry.objects.filter(query, log_id=log_id).order_by('timestamp').distinct()[offset:offset+100]
	# If the user supplies some bogus filter it will be caught here and changed to newest
	else:
		return redirect('/logs/' + str(log_id) + '/?sort=newest&offset=' + str(offset) + "&" + all_filter_str)


def log(request, log_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	try:
		cur_log = Log.objects.get(pk=log_id)
	except ObjectDoesNotExist:
		return render(request, 'patientlogs/object_does_not_exist.html', {'obj_type': 'log'})
	# Make sure the user is a member and can view this log
	if request.user not in cur_log.org.members.all():
		return render(request, 'accounts/not_authorized.html')
	# Get variables from URL that alter view
	# Second argument is default value
	sort = request.GET.get('sort', 'newest')
	res_filter = request.GET.get('resfilter', '')
	tag_filter = request.GET.get('tagfilter', '')
	logger_filter = request.GET.get('loggerfilter', '')
	daterange_filter = request.GET.get('daterangefilter', '')
	all_filter_str = "resfilter=" + res_filter + "&tagfilter=" + tag_filter + "&loggerfilter=" + logger_filter + "&daterangefilter=" + daterange_filter
	try:
		offset = int(request.GET.get('offset', '0'))
	# If the user supplies some bogus offset it will be caught here and changed to zero
	except ValueError:
		return redirect('/logs/' + str(log_id) + '/?sort=' + str(sort) + '&offset=0')
	tags = Tag.objects.filter(org_id=cur_log.org_id)
	residents = Resident.objects.filter(org_id=cur_log.org_id)
	# Helper functions
	# Either redirect or continue
	offset_res = log_resolve_offset(all_filter_str, offset, sort, log_id)
	if offset_res is not None:
		return offset_res
	sort_res = log_resolve_sort_and_filter(all_filter_str, res_filter, tag_filter, logger_filter, daterange_filter, sort, offset, log_id)
	# Either redirect or use the sorted entries
	if sort_res is HttpResponseRedirect:
		return sort_res
	else:
		entries = sort_res
	return render(request, 'patientlogs/log.html', {'log': cur_log, 'entries': entries, 'tags': tags,
													'residents': residents, 'sort': sort, 'offset': offset,
													'resfilter': res_filter, 'tagfilter': tag_filter, 'loggerfilter': logger_filter,
													'daterangefilter': daterange_filter})


def log_detail(request, log_id, entry_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	try:
		cur_log = Log.objects.get(pk=log_id)
	except ObjectDoesNotExist:
		return render(request, 'patientlogs/object_does_not_exist.html', {'obj_type': 'log'})
	# Make sure the user is a member and can view this log
	if request.user not in cur_log.org.members.all():
		return render(request, 'accounts/not_authorized.html')
	# Get variables from URL that alter view
	# Second argument is default value
	sort = request.GET.get('sort', 'newest')
	res_filter = request.GET.get('resfilter', '')
	tag_filter = request.GET.get('tagfilter', '')
	logger_filter = request.GET.get('loggerfilter', '')
	daterange_filter = request.GET.get('daterangefilter', '')
	all_filter_str = "resfilter=" + res_filter + "&tagfilter=" + tag_filter + "&loggerfilter=" + logger_filter + "&daterangefilter=" + daterange_filter
	try:
		offset = int(request.GET.get('offset', '0'))
	# If the user supplies some bogus offset it will be caught here and changed to zero
	except ValueError:
		return redirect('/logs/' + str(log_id) + '/?sort=' + str(sort) + '&offset=0')
	tags = Tag.objects.filter(org_id=cur_log.org_id)
	residents = Resident.objects.filter(org_id=cur_log.org_id)
	# Helper functions
	# Either redirect or continue
	offset_res = log_resolve_offset(all_filter_str, offset, sort, log_id)
	if offset_res is not None:
		return offset_res
	sort_res = log_resolve_sort_and_filter(all_filter_str, res_filter, tag_filter, logger_filter, daterange_filter, sort, offset, log_id)
	# Either redirect or use the sorted entries
	if sort_res is HttpResponseRedirect:
		return sort_res
	else:
		entries = sort_res
	# Get the detail object based on the entry_id
	try:
		detail = Entry.objects.get(pk=entry_id)
	except Entry.DoesNotExist:
		return render(request, 'patientlogs/object_does_not_exist.html', {'obj_type': 'entry'})
	return render(request, 'patientlogs/log.html', {'log': cur_log, 'entries': entries, 'tags': tags,
													'residents': residents, 'detail': detail, 'sort': sort, 'offset': offset,
													'resfilter': res_filter, 'tagfilter': tag_filter,
													'loggerfilter': logger_filter, 'daterangefilter': daterange_filter})


def send_email_alert(entry):
	message = render_to_string('emails/email_alert.html', {
		'entry': entry
	})
	mail_subject = 'Email Alert for Resident Activity'
	to_email = []
	for resident in entry.residents.all():
		for advocate in resident.advocates.all():
			to_email.append(advocate.email)
	email = EmailMultiAlternatives(mail_subject, message, to=to_email)
	email.content_subtype = 'html'
	email.mixed_subtype = 'related'
	email.send()


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
			should_send = False
			for tag in form.clean_tags():
				entry.tags.add(tag)
				if tag.should_email:
					should_send = True
			if should_send:
				send_email_alert(entry)
			return redirect('/logs/' + str(log_id))

	return render(request, 'patientlogs/new_entry.html', {'log': log, 'form': form})
