from django import forms

from patientlog.models import Entry, Resident


class SelectResidentsField(forms.ModelMultipleChoiceField):
	def label_from_instance(self, obj):
		return "%s" % obj.name


class CreateEntryForm(forms.Form):
	message = forms.CharField(max_length=1000, widget=forms.Textarea(
		attrs={'type': 'text',
			'class': 'form-control'}
	))
	residents = SelectResidentsField(
		queryset=None, required=False, widget=forms.SelectMultiple(
		attrs={'type': 'input',
			'class': 'form-control'}
		))

	residents_list = Resident()

	def __init__(self, *args, **kwargs):
		self.residents_list = kwargs.pop('residents', None)
		super(CreateEntryForm, self).__init__(*args, **kwargs)
		self.fields['residents'].queryset = self.residents_list

	def save(self, commit=True):
		return Entry(
			message=self.cleaned_data['message'],
		)

