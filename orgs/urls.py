from django.conf.urls import url, include
from django.views.generic import RedirectView

from orgs import views

urlpatterns = [
	url(r'^(?P<org_id>[0-9]+)/logs/$', views.logs, name='org_logs'),
	url(r'^(?P<org_id>[0-9]+)/tags/$', views.tags, name='org_tags'),
	url(r'^(?P<org_id>[0-9]+)/residents/$', views.residents, name='org_residents'),
	url(r'^(?P<org_id>[0-9]+)/$', views.org, name='org'),
	url(r'^$', RedirectView.as_view(url='/orgs/dash'), name='orgs'),
	url(r'^dash/$', views.org_dash, name='dash'),
	url(r'^create/$', views.create_org, name='create_org'),

]