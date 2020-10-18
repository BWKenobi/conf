from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from .models import Profile


class ProfileUdpateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('surname', 'name', 'name2', 'work_place')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			self.fields[field].required=True


class ProfileAddReprotForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('report_name', 'report_file')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			self.fields[field].required=True
