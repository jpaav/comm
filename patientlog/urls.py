from django.conf.urls import url

from patientlog import views

urlpatterns = [
	url(r'^(?P<log_id>[0-9]+)/$', views.log, name='log'),
	# We should make this start with eventView instead of just having numbers

]