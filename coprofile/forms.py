from django.conf import settings
from django import forms
from datetime import date


from django.contrib.auth.models import User
from .models import CoProfile


class CoProfileUdpateForm(forms.ModelForm):
	class Meta:
		model = CoProfile
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


class CoProfileAddReprotForm(forms.ModelForm):
	class Meta:
		model = CoProfile
		fields = ('report_name', )

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			self.fields[field].required=True


class CoProfileAddReprotFileForm(forms.ModelForm):
	class Meta:
		model = CoProfile
		fields = ('report_file',)

	def __init__(self, *args, **kwargs):
		edit = kwargs.pop('edit', None)
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete':'false'})
			if not edit:
				self.fields[field].required=False


class CoProfileRegistrationForm(forms.Form):
	SPEAKER_TYPE = (
		('1', 'Выступление с докладом (очно)'),
		('4', 'Выступление с докладом (он-лайн)'),
		('2', 'Публикация статьи'),
		('3', 'Участие без доклада'),
	)

	surname = forms.CharField(label = 'Фамилия*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	name  = forms.CharField(label = 'Имя*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	name2  = forms.CharField(label = 'Отчество', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	phone = forms.CharField(label = 'Телефон*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	work_place = forms.CharField(label = 'Название организации*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	work_part = forms.CharField(label = 'Название отдела (факультет, кафедра)', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	position = forms.CharField(label = 'Занимаемая должность', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	degree = forms.CharField(label = 'Ученая степень, ученое звание', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	speaker = forms.ChoiceField(label = 'Форма участия', choices = SPEAKER_TYPE, widget=forms.Select(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)


	def clean(self):
		data = self.cleaned_data
		