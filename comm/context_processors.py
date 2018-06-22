from comm import settings
from patientlog.models import Log


def is_simple_processor(request):
	return {'simple_ui': settings.SIMPLE_UI}


def simple_log(request):
	return {'simple_log': Log.objects.get(pk=settings.SIMPLE_LOG_ID)}
