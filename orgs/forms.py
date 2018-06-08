from django import forms

from orgs.models import Org


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
