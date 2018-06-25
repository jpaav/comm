from comm import settings
from patientlog.models import Log

import os


def is_simple_processor(request):
	return {'simple_ui': settings.SIMPLE_UI}


def simple_log(request):
	try:
		id = int(os.environ['SIMPLE_LOG_ID'])
	except KeyError:
		id = settings.SIMPLE_LOG_ID
	return {'simple_log': Log.objects.get(pk=id)}
