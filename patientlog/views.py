from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from patientlog.forms import CreateEntryForm
from patientlog.models import Log, Entry


def log(request, log_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	try:
		log = Log.objects.get(pk=log_id)
	except ObjectDoesNotExist:
		return render(request, 'patientlogs/log_does_not_exist.html')
	entries = Entry.objects.filter(log=log)
	return render(request, 'patientlogs/log.html', {'log': log, 'entries': entries})


def new_entry(request, log_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	log = Log.objects.get(pk=log_id)
	if request.method == 'GET':
		form = CreateEntryForm()
	else:
		form = CreateEntryForm(request.POST)
		if form.is_valid():
			entry = form.save(commit=False)
			entry.logger = request.user
			entry.log = log
			entry.save()
			return redirect('/log/' + str(log_id))

	return render(request, 'patientlogs/new_entry.html', {'log': log, 'form': form})
