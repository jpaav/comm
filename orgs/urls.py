from django.conf.urls import url, include
from django.views.generic import RedirectView

from orgs import views

urlpatterns = [
	url(r'^(?P<org_id>[0-9]+)/logs/$', views.logs, name='org_logs'),
	url(r'^(?P<org_id>[0-9]+)/tags/$', views.tags, name='org_tags'),
	url(r'^(?P<org_id>[0-9]+)/tags/(?P<tag_id>[0-9]+)/$', views.tags_detail, name='org_tags_detail'),
	url(r'^(?P<org_id>[0-9]+)/tags/(?P<tag_id>[0-9]+)/delete/$', views.tags_delete, name='org_tags_detail_delete'),
	url(r'^(?P<org_id>[0-9]+)/residents/$', views.residents, name='org_residents'),
	url(r'^(?P<org_id>[0-9]+)/residents/(?P<res_id>[0-9]+)/$', views.residents_detail, name='org_residents_detail'),
	url(r'^(?P<org_id>[0-9]+)/residents/(?P<res_id>[0-9]+)/delete/$', views.residents_delete, name='org_residents_delete'),
	url(r'^(?P<org_id>[0-9]+)/$', views.org, name='org'),
	url(r'^$', RedirectView.as_view(url='/orgs/dash'), name='orgs'),
	url(r'^dash/$', views.org_dash, name='dash'),
	# Disabled org creation for the time being
	# url(r'^create/$', views.create_org, name='create_org'),
	url(r'^join/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.join, name='join'),
	url(r'^(?P<org_id>[0-9]+)/approve/(?P<user_id>[0-9]+)/$', views.approve, name='approve'),

]