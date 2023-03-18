from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from .models import Profile


class ProfileUdpateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('surname', 'name', 'name2', 'work_place', 'position', 'speaker')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			self.fields[field].required=False
			#self.fields[field].widget.attrs['disabled'] = 'disabled'
