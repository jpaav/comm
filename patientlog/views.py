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
		return render(request, 'patientlogs/log_does_not_exist.html')
	entries = Entry.objects.filter(log=log)
	return render(request, 'patientlogs/log.html', {'log': log, 'entries': entries})


def log_detail(request, log_id, entry_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	try:
		log = Log.objects.get(pk=log_id)
	except ObjectDoesNotExist:
		return render(request, 'patientlogs/log_does_not_exist.html')
	entries = Entry.objects.filter(log=log)
	detail = Entry.objects.get(pk=entry_id)
	return render(request, 'patientlogs/log.html', {'log': log, 'entries': entries, 'detail': detail})


def new_entry(request, log_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	log = Log.objects.get(pk=log_id)
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
