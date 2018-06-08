from django import forms

from patientlog.models import Entry


class CreateEntryForm(forms.Form):
	message = forms.CharField(max_length=1000, widget=forms.Textarea(
		attrs={'type': 'text',
			'class': 'form-control'}
	))

	def save(self, commit=True):
		return Entry(
			message=self.cleaned_data['message'],
		)

