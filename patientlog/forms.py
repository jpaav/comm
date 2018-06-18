from django import forms

from patientlog.models import Entry, Resident, Tag, Log


class SelectResidentsField(forms.ModelMultipleChoiceField):
	def label_from_instance(self, obj):
		return "%s" % obj.name


class SelectTagsField(forms.ModelMultipleChoiceField):
	def label_from_instance(self, obj):
		return "%s" % obj.title


class CreateEntryForm(forms.Form):
	log = Log()
	message = forms.CharField(max_length=1000, widget=forms.Textarea(
		attrs={'type': 'text',
			'class': 'form-control'}
	))
	residents = SelectResidentsField(
		queryset=None, required=False, widget=forms.SelectMultiple(
		attrs={'type': 'input',
			'class': 'form-control'}
		))
	tags = SelectTagsField(
		queryset=None, required=False, widget=forms.SelectMultiple(
		attrs={'type': 'input',
			'class': 'form-control'}
		))

	def clean_residents(self):
		residents = self.cleaned_data['residents']
		return residents

	def clean_tags(self):
		tags = self.cleaned_data['tags']
		return tags

	def __init__(self, *args, **kwargs):
		self.log = kwargs.pop('log', None)
		super(CreateEntryForm, self).__init__(*args, **kwargs)
		self.fields['residents'].queryset = Resident.objects.filter(org=self.log.org)
		self.fields['tags'].queryset = Tag.objects.filter(org=self.log.org)

	def save(self, commit=True):
		return Entry(
			message=self.cleaned_data['message'],
			log=self.log,
		)

