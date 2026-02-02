from django.conf import settings
from django import forms
from datetime import date

from django.contrib.auth.models import User
from .models import Answer


class AnswerForm(forms.ModelForm):
	class Meta:
		model = Answer
		fields = ('answer_1', 'answer_2', 'answer_3')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			self.fields[field].required=True

