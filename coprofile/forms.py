from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from .models import CoProfile


class CoProfileUdpateForm(forms.ModelForm):
	class Meta:
		model = CoProfile
		fields = ('surname', 'name', 'name2', 'work_place', 'position', 'speaker')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			self.fields[field].required=False
			#self.fields[field].widget.attrs['disabled'] = 'disabled'


class CoProfileRegistrationForm(forms.Form):
	SPEAKER_TYPE = (
		('1', 'Докладчик'),
		('2', 'Участник'),
	)

	surname = forms.CharField(label = 'Фамилия*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	name  = forms.CharField(label = 'Имя*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	name2  = forms.CharField(label = 'Отчество', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	work_place = forms.CharField(label = 'Название организации*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	position = forms.CharField(label = 'Занимаемая должность*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	speaker = forms.ChoiceField(label = 'Форма участия', choices = SPEAKER_TYPE, initial = '2', widget=forms.Select(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)


	def clean(self):
		data = self.cleaned_data
		