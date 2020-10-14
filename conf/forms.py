from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User as UserModel
from django.contrib.auth.models import User
	
from profileuser.models import Profile

User = get_user_model()


class UserLoginForm(forms.Form):
	email = forms.EmailField(label = 'E-Mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
	password = forms.CharField(label = 'Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


	def clean(self, *args, **kwargs):
		email = self.cleaned_data.get('email')
		password = self.cleaned_data.get('password')
		
		if email and password:
			vaild_user = User.objects.filter(username=email)

			if not vaild_user:
				raise forms.ValidationError('Пользователь не существует!')

			if not vaild_user[0].is_active:
				raise forms.ValidationError('Адрес электронной почты не подтвержден!')

			user = authenticate(username = email, password = password)

			if not user:
				raise forms.ValidationError('Неверный пароль!')

		return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
	email = forms.EmailField(label = 'Ваш e-mail*', widget=forms.EmailInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	name  = forms.CharField(label = 'Ваше имя*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	name2  = forms.CharField(label = 'Ваше отчество*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	surname = forms.CharField(label = 'Ваша фамилия*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	work_place = forms.CharField(label = 'Место работы (полностью)*', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)
	password = forms.CharField(label = 'Задайте пароль*', widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete':'false'}), required=True)

	def __init__(self, *args, **kwargs):
		super(UserRegistrationForm, self).__init__(*args, **kwargs)


	class Meta:
		model = User
		fields = ('email',)


	def clean(self):
		data = self.cleaned_data
		email = data.get('email')

		try:
			vaild_user = UserModel.objects.get(username=email)
		except UserModel.DoesNotExist:
			if email and UserModel.objects.filter(email=email).count()>0:
				raise forms.ValidationError('Используйте другой адрес электронной почты!')
			return data

		raise forms.ValidationError('Пользователь с таким email существует!')


class ChangePasswordForm(forms.Form):
	oldpassword = forms.CharField(label = 'Старый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), required=False)
	newpassword = forms.CharField(label = 'Новый пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'autocomplete': 'off'}), required=False)


	def clean(self):
		oldpass = self.cleaned_data['oldpassword']
		newpass = self.cleaned_data['newpassword']

		if oldpass and newpass:
			user = authenticate(username = self.username, password = oldpass)
			if user is None:
				raise forms.ValidationError('Неверный пароль!')
		return self.cleaned_data


class CustomPasswordResetForm(PasswordResetForm):
	class Meta:
		model = User
		fields = ['email']

	def __init__(self, *args, **kwargs):
		super(CustomPasswordResetForm, self).__init__(*args, **kwargs)
		self.fields['email'].widget.attrs.update({'class': 'form-control'})
		self.fields['email'].label = ''


class CustomSetPasswordForm(SetPasswordForm):
	new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

	def __init__(self, *args, **kwargs):
		super(CustomSetPasswordForm, self).__init__(*args, **kwargs)
		self.fields['new_password1'].label = 'Пароль'
		self.fields['new_password2'].label = 'Пароль еще раз'


	def clean_new_password2(self):
		password1 = self.cleaned_data.get('new_password1')
		password2 = self.cleaned_data.get('new_password1')
		return password2


