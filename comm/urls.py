"""comm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.conf.urls import url, include
	2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import RedirectView

from comm import settings

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^login/$', auth_views.login, {'template_name': 'accounts/login.html'}, name='login'),
	url(r'^logout/$', auth_views.logout, {'next_page': '/accounts/logout_lander'}, name='logout'),
	url(r'^accounts/', include('accounts.urls', namespace='accounts')),
	url(r'^rooms/', include('rooms.urls', namespace='rooms')),
	url(r'^orgs/', include('orgs.urls', namespace='orgs')),
	url(r'^logs/', include('patientlog.urls', namespace='patientlog')),
	url(r'^$', RedirectView.as_view(url='/login/'), name='index')
]
