from django import forms

from orgs.models import Org
from patientlog.models import Tag, Resident


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
	title = forms.CharField(required=True, widget=forms.TextInput(
		attrs={'type': 'text',
			'class': 'form-control'}))

	color = forms.CharField(required=True, widget=forms.TextInput(
		attrs={'type': 'text',
			'class': 'form-control'}))

	def clean_title(self):
		title = self.cleaned_data['title']
		return title

	def save(self, commit=True):
		return Tag(
			title=self.cleaned_data['title'],
			color=self.cleaned_data['color'],
		)


class CreateResidentForm(forms.Form):
	name = forms.CharField(required=True, widget=forms.TextInput(
		attrs={'type': 'text',
			'class': 'form-control'}))

	def clean_name(self):
		name = self.cleaned_data['name']
		return name

	def save(self, commit=True):
		return Resident(
			name=self.cleaned_data['name']
		)
