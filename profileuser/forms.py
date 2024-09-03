from django.conf import settings
from datetime import date

from django import forms
from django.contrib.auth.models import User
from .models import Profile


class ProfileUdpateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('surname', 'name', 'name2', 'phone', 'work_place', 'work_part', 'position', 'degree', 'speaker')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		dte = date.today()
		dte_deadline = date(2024,10,14)
		report_flag = False
		if dte<dte_deadline:
			report_flag = True

		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			self.fields[field].required=False

			if not report_flag:
				self.fields[field].widget.attrs['disabled'] = 'disabled'


class ProfileAddReprotForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('report_name',)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			self.fields[field].required=True


class ProfileAddReprotFileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('report_file',)

	def __init__(self, *args, **kwargs):
		edit = kwargs.pop('edit', None)
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			if not edit:
				self.fields[field].required=True