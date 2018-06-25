from datetime import datetime

from django import forms

from orgs.models import Org
from patientlog.models import Tag, Resident


class SelectResidentsField(forms.ModelMultipleChoiceField):
	def label_from_instance(self, obj):
		return "%s" % obj.get_full_name()


class CreateOrgForm(forms.Form):
	name = forms.CharField(required=True, widget=forms.TextInput(
		attrs={'type': 'text',
			'class': 'form-control'}))
	description = forms.CharField(required=False, widget=forms.TextInput(
		attrs={'type': 'text',
			'class': 'form-control'}))
	location = forms.CharField(required=False, widget=forms.TextInput(
		attrs={'type': 'text',
			'class': 'form-control'}))

	def clean_location(self):
		location = self.cleaned_data['location']
		return location

	def clean_name(self):
		name = self.cleaned_data['name']
		return name

	def clean_description(self):
		description = self.cleaned_data['description']
		return description

	def save(self, commit=True):
		return Org(
			name=self.cleaned_data['name'],
			description=self.cleaned_data['description'],
			location=self.cleaned_data['location']
		)


class CreateTagForm(forms.Form):
	IMPORTANCE_CHOICES = [
		('1', '!'),
		('2', '!!'),
		('3', '!!!'),
	]
	title = forms.CharField(required=True, widget=forms.TextInput(
		attrs={'type': 'text',
			'class': 'form-control'}))

	color = forms.CharField(required=True, widget=forms.TextInput(
		attrs={'type': 'text',
			'class': 'form-control'}))

	importance = forms.ChoiceField(required=True, initial=1, choices=IMPORTANCE_CHOICES, widget=forms.Select(
		attrs={'type': 'text',
			'class': 'form-control'}))

	should_email = forms.NullBooleanField(required=False, widget=forms.NullBooleanSelect(
		attrs={'type': 'text',
			'class': 'form-control'}))

	def clean_title(self):
		title = self.cleaned_data['title']
		return title

	def clean_color(self):
		color = self.cleaned_data['color']
		# Remove hashtag if present
		if color[0] == '#':
			color = color[:-1]
		if not len(color) == 6:
			color = 'e9ecef'
		try:
			int(color, 16)
		except ValueError:
			color = 'e9ecef'
		return color

	def save(self, commit=True):
		return Tag(
			title=self.cleaned_data['title'],
			color=self.clean_color(),
			importance=self.cleaned_data['importance'],
			should_email=self.cleaned_data['should_email']
		)


class CreateResidentForm(forms.Form):

	org = Org()

	name = forms.CharField(required=True, widget=forms.TextInput(
		attrs={'type': 'text',
			'class': 'form-control'}))

	room = forms.CharField(required=False, widget=forms.TextInput(
		attrs={'type': 'text',
			'class': 'form-control'}))

	timestamp_admitted = forms.DateTimeField(label='Last Admitted', initial=datetime.now(), required=False, input_formats=['%Y-%m-%dT%H:%M'], widget=forms.DateTimeInput(
		attrs={'type': 'datetime-local',
			'class': 'form-control'}))

	timestamp_left = forms.DateTimeField(label='Last left', initial=datetime.now(), required=False, input_formats=['%Y-%m-%dT%H:%M'], widget=forms.DateTimeInput(
		attrs={'type': 'datetime-local',
			'class': 'form-control'}))

	advocates = SelectResidentsField(
		queryset=None, required=False, widget=forms.SelectMultiple(
			attrs={'type': 'input',
				'class': 'form-control'}))

	def clean_name(self):
		name = self.cleaned_data['name']
		return name

	def clean_room(self):
		room = self.cleaned_data['room']
		return room

	def __init__(self, *args, **kwargs):
		self.org = kwargs.pop('org', None)
		super(CreateResidentForm, self).__init__(*args, **kwargs)
		if self.org:
			self.fields['advocates'].queryset = self.org.members.all()

	def save(self, commit=True):
		return Resident(
			name=self.cleaned_data['name'],
			room=self.cleaned_data['room'],
			timestamp_admitted=self.cleaned_data['timestamp_admitted'],
			timestamp_left=self.cleaned_data['timestamp_left'],
		)


class UpdateTagForm(forms.Form):
	IMPORTANCE_CHOICES = [
		('1', '!'),
		('2', '!!'),
		('3', '!!!'),
	]

	title = forms.CharField(required=True, widget=forms.TextInput(
		attrs={'type': 'text',
				'class': 'form-control'}))

	color = forms.CharField(required=True, widget=forms.TextInput(
		attrs={'type': 'text',
				'class': 'form-control'}))

	importance = forms.ChoiceField(required=True, initial=1, choices=IMPORTANCE_CHOICES, widget=forms.Select(
		attrs={'type': 'text',
			'class': 'form-control'}))

	should_email = forms.NullBooleanField(required=False, widget=forms.NullBooleanSelect(
		attrs={'type': 'text',
			'class': 'form-control'}))

	def clean_color(self):
		color = self.cleaned_data['color']
		# Remove hashtag if present
		if color[0] == '#':
			color = color[1:]
		if not len(color) == 6:
			color = 'e9ecef'
		try:
			int(color, 16)
		except ValueError:
			color = 'e9ecef'
		return color

	def save(self, commit=True):
		return Tag(
			title=self.cleaned_data['title'],
			color=self.clean_color(),
			importance=self.cleaned_data['importance'],
			should_email=self.cleaned_data['should_email']
		)


class UpdateResidentForm(forms.Form):

	org = Org()

	name = forms.CharField(required=True, widget=forms.TextInput(
		attrs={'type': 'text',
			'class': 'form-control'}))

	room = forms.CharField(required=False, widget=forms.TextInput(
		attrs={'type': 'text',
			'class': 'form-control'}))

	timestamp_admitted = forms.DateTimeField(label='Last Admitted', initial=datetime.now(), required=False, input_formats=['%Y-%m-%dT%H:%M'], widget=forms.DateTimeInput(
		attrs={'type': 'datetime-local',
			'class': 'form-control'}))

	timestamp_left = forms.DateTimeField(label='Last left', initial=datetime.now(), required=False, input_formats=['%Y-%m-%dT%H:%M'], widget=forms.DateTimeInput(
		attrs={'type': 'datetime-local',
			'class': 'form-control'}))

	advocates = SelectResidentsField(
		queryset=None, required=False, widget=forms.SelectMultiple(
			attrs={'type': 'input',
				'class': 'form-control'}))

	def __init__(self, *args, **kwargs):
		self.org = kwargs.pop('org', None)
		super(UpdateResidentForm, self).__init__(*args, **kwargs)
		if self.org:
			self.fields['advocates'].queryset = self.org.members.all()

	def save(self, commit=True):
		return self.cleaned_data
