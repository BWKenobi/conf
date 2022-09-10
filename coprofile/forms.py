from django.conf import settings
from django import forms
from django.contrib.auth.models import User
from .models import CoProfile


class CoProfileUdpateForm(forms.ModelForm):
	class Meta:
		model = CoProfile
		fields = ('surname', 'name', 'name2', 'phone', 'work_place', 'work_part', 'position', 'degree')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			self.fields[field].required=False
			#self.fields[field].widget.attrs['disabled'] = 'disabled'


class CoProfileAddReprotForm(forms.ModelForm):
	class Meta:
		model = CoProfile
		fields = ('report_name', 'report_file')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			self.fields[field].required=True


class CoProfileRegistrationForm(forms.Form):
	SPEAKER_TYPE = (
		('1', 'Выступление с докладом'),
		('2', 'Публикация статьи'),
		('3', 'Участие без доклада'),
	)

	name  = forms.CharField(label = 'Имя*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	name2  = forms.CharField(label = 'Отчество', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	surname = forms.CharField(label = 'Фамилия*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	phone = forms.CharField(label = 'Телефон*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	work_place = forms.CharField(label = 'Название организации*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	work_part = forms.CharField(label = 'Название отдела (факультет, кафедра)', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	position = forms.CharField(label = 'Занимаемая должность', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	degree = forms.CharField(label = 'Ученая степень, ученое звание', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	speaker = forms.ChoiceField(label = 'Форма участия', choices = SPEAKER_TYPE, widget=forms.Select(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)


	def clean(self):
		data = self.cleaned_data
		