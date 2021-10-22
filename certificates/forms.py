from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User as UserModel
from django.contrib.auth.models import User
	
User = get_user_model()


class MakeCertificateForm(forms.Form):
	CHOICES = (
		(' ', ' '),
		('-', '-'),
		('/', '/')
	)

	iterable  = forms.CharField(label = 'Переменная часть номера *', widget=forms.TextInput(attrs={'type': 'number', 'class': 'form-control', 'autocomplete':'false'}), required=False)
	divider  = forms.ChoiceField(label = 'Разделитель', choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control', 'autocomplete':'false'}), required=False)
	noniterable  = forms.CharField(label = 'Неизменная часть номера', widget=forms.TextInput(attrs={'type': 'number', 'class': 'form-control', 'autocomplete':'false'}), required=False)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
