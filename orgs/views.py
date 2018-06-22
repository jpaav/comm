from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from comm import settings
from orgs.forms import CreateOrgForm, CreateTagForm, CreateResidentForm, UpdateTagForm, UpdateResidentForm
from orgs.models import Org
from orgs.tokens import join_org_token
from patientlog.models import Log, Tag, Resident


def org(request, org_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	try:
		org = Org.objects.get(pk=org_id)
	except Org.DoesNotExist:
		return render(request, 'patientlogs/object_does_not_exist.html', {'obj_type': 'org'})
	if request.user not in org.members.all():
		return render(request, 'accounts/not_authorized.html')
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
	approved_orgs = Org.objects.filter(members=request.user)
	unapproved_orgs = Org.objects.filter(unapproved=request.user)
	return render(request, 'orgs/org_dash.html', {'approved_orgs': approved_orgs, 'unapproved_orgs': unapproved_orgs})


def logs(request, org_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	try:
		org = Org.objects.get(pk=org_id)
	except Org.DoesNotExist:
		return render(request, 'patientlogs/object_does_not_exist.html', {'obj_type': 'org'})
	if request.user not in org.members.all():
		return render(request, 'accounts/not_authorized.html')
	logs = Log.objects.filter(org=org)
	if logs.count() == 1 and settings.SIMPLE_UI:
		return redirect('/logs/' + str(logs.first().id))
	return render(request, 'orgs/logs.html', {'logs': logs})


def tags(request, org_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	org = Org.objects.get(pk=org_id)
	if not request.user == org.owner:
		return render(request, 'accounts/not_authorized.html')
	tags = Tag.objects.filter(org=org)
	if request.method == 'GET':
		create_form = CreateTagForm()
	else:
		create_form = CreateTagForm(request.POST)
		if create_form.is_valid():
			tag = create_form.save(commit=False)
			tag.org = org
			tag.save()
	return render(request, 'orgs/tags.html', {'create_form': create_form, 'tags': tags})


def residents(request, org_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	try:
		org = Org.objects.get(pk=org_id)
	except Org.DoesNotExist:
		return render(request, 'patientlogs/object_does_not_exist.html', {'obj_type': 'org'})
	residents = Resident.objects.filter(org=org)
	if request.user not in org.members.all():
		return render(request, 'accounts/not_authorized.html')
	if request.method == 'GET':
		create_form = CreateResidentForm()
	else:
		create_form = CreateResidentForm(request.POST)
		if create_form.is_valid():
			resident = create_form.save(commit=False)
			resident.org = org
			resident.save()
	return render(request, 'orgs/residents.html', {'create_form': create_form, 'residents': residents})


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
	if org.unapproved.filter(pk=request.user.id).exists():
		return HttpResponse('You are already unapproved for this organization.')
	if org.members.filter(pk=request.user.id).exists():
		return HttpResponse('You are already a member for this organization.')
	if org is not None and join_org_token.check_token(org, token):
		# Adds current user to org
		org.unapproved.add(request.user)
		return render(request, 'orgs/join_confirmed.html', {'org_name': org.name})
	else:
		return HttpResponse('Activation link is invalid!')


def approve(request, org_id, user_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	try:
		org = Org.objects.get(pk=org_id)
	except Org.DoesNotExist:
		return render(request, 'patientlogs/object_does_not_exist.html', {'obj_type': 'org'})
	try:
		user = User.objects.get(pk=user_id)
	except User.DoesNotExist:
		return render(request, 'patientlogs/object_does_not_exist.html', {'obj_type': 'user'})
	if request.user == org.owner:
		if org.unapproved.get(pk=user_id) is not None:
			org.unapproved.remove(user)
			org.members.add(user)
		return redirect('/orgs/' + str(org_id))
	else:
		return render(request, 'accounts/not_authorized.html')


def residents_detail(request, org_id, res_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	org = Org.objects.get(pk=org_id)
	try:
		detail = Resident.objects.get(pk=res_id)
	except Resident.DoesNotExist:
		return render(request, 'patientlogs/object_does_not_exist.html', {'obj_type': 'resident'})
	residents = Resident.objects.filter(org=org)
	if request.method == 'GET':
		create_form = CreateResidentForm()
		update_form = UpdateResidentForm(
			initial={
				'name': detail.name,
				'room': detail.room,
				'timestamp_admitted': detail.timestamp_admitted,
				'timestamp_left': detail.timestamp_left
			}
		)
	else:
		create_form = CreateResidentForm(request.POST)
		update_form = UpdateResidentForm(request.POST)
		if update_form.is_valid():
			update = update_form.save(commit=False)
			detail.name = update['name']
			detail.room = update['room']
			detail.timestamp_admitted = update['timestamp_admitted']
			detail.timestamp_left = update['timestamp_left']
			detail.save()
			return redirect('/orgs/' + str(org_id) + '/residents/' + str(res_id))
		if create_form.is_valid():
			resident = create_form.save(commit=False)
			resident.org = org
			resident.save()
			return redirect('/orgs/' + str(org_id) + '/residents/' + str(res_id))
	return render(request, 'orgs/residents.html',
	              {'create_form': create_form, 'update_form': update_form, 'residents': residents, 'detail': detail})


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
		create_form = CreateTagForm()
		update_form = UpdateTagForm(
			initial={
				'title': detail.title,
				'color': detail.color
			}
		)
	else:
		create_form = CreateTagForm(request.POST)
		update_form = UpdateTagForm(request.POST)
		if update_form.is_valid():
			update = update_form.save(commit=False)
			detail.title = update.title
			detail.color = update.color
			detail.save()
			return redirect('/orgs/' + str(org_id) + '/tags/' + str(tag_id))
		if create_form.is_valid():
			tag = create_form.save(commit=False)
			tag.org = org
			tag.save()
			return redirect('/orgs/' + str(org_id) + '/tags/' + str(tag_id))
	return render(request, 'orgs/tags.html',
	              {'create_form': create_form, 'update_form': update_form, 'tags': tags, 'detail': detail})


def unapprove(request, org_id, user_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	try:
		org = Org.objects.get(pk=org_id)
	except Org.DoesNotExist:
		return render(request, 'patientlogs/object_does_not_exist.html', {'obj_type': 'org'})
	try:
		user = User.objects.get(pk=user_id)
	except User.DoesNotExist:
		return render(request, 'patientlogs/object_does_not_exist.html', {'obj_type': 'user'})
	if request.user == org.owner:
		if org.members.get(pk=user_id) is not None:
			org.members.remove(user)
			org.unapproved.add(user)
		return redirect('/orgs/' + str(org_id))
	else:
		return render(request, 'accounts/not_authorized.html')


def remove_unapproved(request, org_id, user_id):
	if not request.user.is_authenticated():
		return redirect('/login/')
	try:
		org = Org.objects.get(pk=org_id)
	except Org.DoesNotExist:
		return render(request, 'patientlogs/object_does_not_exist.html', {'obj_type': 'org'})
	try:
		user = User.objects.get(pk=user_id)
	except User.DoesNotExist:
		return render(request, 'patientlogs/object_does_not_exist.html', {'obj_type': 'user'})
	if request.user == org.owner:
		if org.unapproved.get(pk=user_id) is not None:
			org.unapproved.remove(user)
		return redirect('/orgs/' + str(org_id))
	else:
		return render(request, 'accounts/not_authorized.html')
