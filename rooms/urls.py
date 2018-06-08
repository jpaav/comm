from django.conf.urls import url

from rooms import views

urlpatterns = [
	url(r'^(?P<room_id>[0-9]+)/$', views.room, name='room'),
	# We should make this start with eventView instead of just having numbers

]