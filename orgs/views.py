from django.shortcuts import render, redirect

from orgs.forms import CreateOrgForm
from orgs.models import Org
from patientlog.models import Log


def org(request, org_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	org = Org.objects.filter(pk=org_id)
	return render(request, 'orgs/org.html')


def create_org(request):
	if not request.user.is_authenticated():
		return redirect('/login/')
	if request.method == 'GET':
		form = CreateOrgForm()
	else:
		form = CreateOrgForm(request.POST)
		if form.is_valid():
			org = form.save(commit=False)
			org.owner = request.user
			org.save()
			return redirect('/orgs/')
	return render(request, 'orgs/create_org.html', {'form': form})


def org_dash(request):
	if not request.user.is_authenticated():
		return redirect('/login/')
	orgs = Org.objects.filter(members=request.user) | Org.objects.filter(owner=request.user)
	return render(request, 'orgs/org_dash.html', {'orgs': orgs})


def logs(request, org_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	logs = Log.objects.filter(org=Org.objects.filter(pk=org_id))
	return render(request, 'orgs/logs.html', {'logs': logs})
