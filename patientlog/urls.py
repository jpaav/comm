from django.conf.urls import url

from patientlog import views

urlpatterns = [
	url(r'^(?P<log_id>[0-9]+)/$', views.log, name='log'),
	url(r'^(?P<log_id>[0-9]+)/entry/(?P<entry_id>[0-9]+)/$', views.log_detail, name='log_detail'),
	url(r'^(?P<log_id>[0-9]+)/new_entry/$', views.new_entry, name='new_entry'),
]