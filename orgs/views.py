from django.shortcuts import render, redirect

from orgs.forms import CreateOrgForm, CreateTagForm, CreateResidentForm
from orgs.models import Org
from patientlog.models import Log, Tag, Resident


def org(request, org_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	org = Org.objects.get(pk=org_id)
	return render(request, 'orgs/org.html', {'org': org})


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


def tags(request, org_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	org = Org.objects.get(pk=org_id)
	tags = Tag.objects.filter(org=org)
	if request.method == 'GET':
		form = CreateTagForm()
	else:
		form = CreateTagForm(request.POST)
		if form.is_valid():
			tag = form.save(commit=False)
			tag.org = org
			tag.save()
	return render(request, 'orgs/tags.html', {'form': form, 'tags': tags})


def residents(request, org_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	org = Org.objects.get(pk=org_id)
	residents = Resident.objects.filter(org=org)
	if request.method == 'GET':
		form = CreateResidentForm()
	else:
		form = CreateResidentForm(request.POST)
		if form.is_valid():
			resident = form.save(commit=False)
			resident.org = org
			resident.save()
	return render(request, 'orgs/residents.html', {'form': form, 'residents': residents})
