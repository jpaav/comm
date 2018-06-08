from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

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
