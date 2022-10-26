from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User as UserModel
from django.contrib.auth.models import User
	
User = get_user_model()


class InfoMailForm(forms.Form):
	theme  = forms.CharField(label = 'Тема рассылки', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	msg  = forms.CharField(label = 'Текст рассылки', widget=forms.Textarea(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	signature  = forms.CharField(label = 'Подпись', widget=forms.Textarea(attrs={'class': 'form-control', 'autocomplete':'false', 'rows': '3'}), required=False)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['signature'].widget.attrs['placeholder'] = 'С уважением,\nавторы портала - AstVisionScience'