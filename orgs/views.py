from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from orgs.forms import CreateOrgForm, CreateTagForm, CreateResidentForm
from orgs.models import Org
from orgs.tokens import join_org_token
from patientlog.models import Log, Tag, Resident


def org(request, org_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	org = Org.objects.get(pk=org_id)
	if request.user == org.owner:
		uid = urlsafe_base64_encode(force_bytes(org.pk))
		token = join_org_token.make_token(org)
		return render(request, 'orgs/org.html', {'org': org, 'uid': uid, 'token': token,
												'domain': get_current_site(request).domain})
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
	orgs = Org.objects.filter(members=request.user)
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
	if not request.user == org.owner:
		return render(request, 'accounts/not_authorized.html')
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
	if not request.user == org.owner:
		return render(request, 'accounts/not_authorized.html')
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


def join(request, uidb64, token):
	if not request.user.is_authenticated():
		return redirect('/login/')
	# Tries to decode the uid and use it as a key to find a user
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		org = Org.objects.get(pk=uid)
	# Catches if the activation link is bad
	except(TypeError, ValueError, OverflowError, Org.DoesNotExist):
		org = None
	if org is not None and join_org_token.check_token(org, token):
		# Adds current user to org
		org.unapproved.add(request.user)
		return render(request, 'orgs/join_confirmed.html', {'org_name': org.name})
	else:
		return HttpResponse('Activation link is invalid!')


def approve(request, org_id, user_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	org = Org.objects.get(pk=org_id)
	user = User.objects.get(pk=user_id)
	if request.user == org.owner:
		if org.unapproved.get(pk=user_id) is not None:
			org.unapproved.remove(user)
			org.members.add(user)
			return redirect('/orgs/' + str(org_id))
		else:
			return HttpResponse('This member is not unapproved.')
	else:
		return HttpResponse('You are not the owner of this org and cannot approve members.')


def residents_detail(request, org_id, res_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	org = Org.objects.get(pk=org_id)
	if not request.user == org.owner:
		return render(request, 'accounts/not_authorized.html')
	try:
		detail = Resident.objects.get(pk=res_id)
	except Resident.DoesNotExist:
		return render(request, 'patientlogs/object_does_not_exist.html', {'obj_type': 'resident'})
	residents = Resident.objects.filter(org=org)
	if request.method == 'GET':
		form = CreateResidentForm()
	else:
		form = CreateResidentForm(request.POST)
		if form.is_valid():
			resident = form.save(commit=False)
			resident.org = org
			resident.save()
	return render(request, 'orgs/residents.html', {'form': form, 'residents': residents, 'detail': detail})


def residents_delete(request, org_id, res_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	org = Org.objects.get(pk=org_id)
	if not request.user == org.owner:
		return render(request, 'accounts/not_authorized.html')
	try:
		resident = Resident.objects.get(pk=res_id)
		resident.delete()
	except Resident.DoesNotExist:
		return render(request, 'patientlogs/object_does_not_exist.html', {'obj_type': 'resident'})
	return redirect('/orgs/' + str(org_id) + '/residents/')


def tags_delete(request, org_id, tag_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	org = Org.objects.get(pk=org_id)
	if not request.user == org.owner:
		return render(request, 'accounts/not_authorized.html')
	try:
		tag = Tag.objects.get(pk=tag_id)
		tag.delete()
	except Tag.DoesNotExist:
		return render(request, 'patientlogs/object_does_not_exist.html', {'obj_type': 'tag'})
	return redirect('/orgs/' + str(org_id) + '/tags/')


def tags_detail(request, org_id, tag_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	org = Org.objects.get(pk=org_id)
	if not request.user == org.owner:
		return render(request, 'accounts/not_authorized.html')
	try:
		detail = Tag.objects.get(pk=tag_id)
	except Tag.DoesNotExist:
		return render(request, 'patientlogs/object_does_not_exist.html', {'obj_type': 'resident'})
	tags = Tag.objects.filter(org=org)
	if request.method == 'GET':
		form = CreateTagForm()
	else:
		form = CreateTagForm(request.POST)
		if form.is_valid():
			tag = form.save(commit=False)
			tag.org = org
			tag.save()
	return render(request, 'orgs/tags.html', {'form': form, 'tags': tags, 'detail': detail})
