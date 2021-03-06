from email.mime.image import MIMEImage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from .models import Profile

from django.contrib.auth import update_session_auth_hash


# The profile page for the current user
def profile(request):
	if not request.user.is_authenticated():
		return redirect('/login/')
	user_orgs = Org.objects.filter(members=request.user)
	return render(request, "accounts/profile.html", {'user': request.user, 'this_user': True, 'orgs': user_orgs})


# Currently disabled but ready to be implemented if wanted
def other_profile(request, user_id):
	return redirect('/accounts/profile/')
	# noinspection PyUnreachableCode
	if not request.user.is_authenticated():
		return redirect('/login/')
	user = User.objects.get(id=user_id)
	if user != request.user:
		profile = Profile.objects.get(user=user)
		return render(request, 'accounts/profile.html',
						{'user': user, 'profile': profile, 'this_user': False})
	else:
		return redirect('/accounts/profile/')


def edit_profile(request):
	if not request.user.is_authenticated():
		return redirect('/login/')
	profile = request.user.profile
	if request.POST:
		form = EditProfileForm(request.POST, profile=profile)
		form2 = EditUserForm(request.POST, instance=request.user)
		if form.is_valid() and form2.is_valid():
			profile.bio = form.save(commit=False)
			profile.save()
			form2.save()
			return redirect('/accounts/profile/')
	form = EditProfileForm(initial={'bio': profile.bio})
	form2 = EditUserForm(instance=request.user)

	return render(request, 'accounts/edit_profile.html', {"form": form, 'profile': profile, "form2": form2})


def edit_password(request):
	if not request.user.is_authenticated():
		return redirect('/login/')
	user = request.user
	form = PasswordChangeForm(user=request.user, data=request.POST)
	if request.POST:
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, user)

			return redirect('/accounts/profile')

	return render(request, 'accounts/edit_password.html', {"form": form})


# The signup page
def signup(request):
	# Checks if the user is sending their data (POST) or getting the form (GET)
	if request.method == 'POST':
		form = SignupForm(request.POST)
		# Makes sure the user filled out the form correctly as dictated by forms.py
		if form.is_valid():
			user = form.save(commit=False)
			# Sets the user to unactivated until they confirm email
			user.is_active = False
			# Saves the user to the server
			user.save()
			# Gets the current domain in order to send the email
			current_site = get_current_site(request)
			# Sends the user an email based on the email template and the info passed in here
			message = render_to_string('emails/activate_account.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			mail_subject = 'Activate your Comm Account!'
			to_email = form.cleaned_data.get('email')
			email = EmailMultiAlternatives(mail_subject, message, to=[to_email])
			email.content_subtype = 'html'
			email.mixed_subtype = 'related'
			fp = open('static/img/test-user-icon.jpg', 'rb')
			logo = MIMEImage(fp.read())
			logo.add_header('Content-ID', '<logo>')
			email.attach(logo)
			email.send()
			return render(request, 'accounts/please_confirm.html')
	else:
		form = SignupForm()

	return render(request, 'accounts/signup.html', {'form': form})


# The activation page for new users
# The uidb64 and token are generated in signup
def activate(request, uidb64, token):
	# Tries to decode the uid and use it as a key to find a user
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
		# Sets the profile's primary key to be the same as the user's
		profile = Profile(username=user.get_username())
	# Catches if the activation link is bad
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user is not None and account_activation_token.check_token(user, token):
		# Sets the user to active
		user.is_active = True
		user.save()
		# profile.save()
		user.backend = 'django.contrib.auth.backends.ModelBackend'
		login(request, user)
		return render(request, 'accounts/account_confirmed.html')
	else:
		return HttpResponse('Activation link is invalid!')


def logoutLander(request):
	return redirect('/login')
