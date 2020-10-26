import os
from pytils import translit

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

def make_upload_path(instance, filename):
	names = filename.split('.')
	new_filename = ''
	for name in names:
		if name != names[0]:
			new_filename += '.'
		new_filename += translit.slugify(name)

	path = 'reports/%s' % new_filename

	return path


def make_certificate_path(instance, filename):
	names = filename.split('.')
	new_filename = ''
	for name in names:
		if name != names[0]:
			new_filename += '.'
		new_filename += translit.slugify(name)

	path = 'reports/sertificate/%s' % new_filename

	return path


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None, blank=True)
	username = models.CharField("Username:", max_length=30, blank=True)

	surname = models.CharField(verbose_name="Фамилия*", max_length=50, blank=True)
	name = models.CharField(verbose_name="Имя*", max_length=30, blank=True)
	name2 = models.CharField(verbose_name="Отчество*", max_length=30, blank=True)
	work_place = models.TextField(verbose_name="Место работы (полностью)*", blank=True)

	certificate_num = models.CharField(verbose_name="Номер сертификата", max_length=30, blank=True)
	certificate_file = models.FileField(verbose_name='Сертификат', blank=True, null=True, upload_to = make_certificate_path)

	speaker= models.BooleanField("Докладчик", default=False)
	report_name = models.CharField(verbose_name="Тема доклада*", max_length=250, blank=True)
	report_file = models.FileField(verbose_name='Файл научной статьи*', blank=True, null=True, upload_to = make_upload_path)

	registration_date = models.DateField(verbose_name="Дата регистрации", default=timezone.now)
	admin_access= models.BooleanField("Права администратора", default=False)
	moderator_access= models.BooleanField("Права модератора", default=False)


	def __str__(self):
		if self.user.is_active:
			return self.username
		return self.username + ' (not active)'


	def get_name(self):
		admin = ''
		if self.admin_access:
			admin = ' (Администратор)'
		if self.surname:
			if self.name2:
				return self.surname + ' ' + self.name[0] + '.' + self.name2[0]+ '.' + admin
			return self.surname + ' ' + self.name[0]+ '.'  + admin

		return self.name + admin


	def get_full_name(self):
		if self.surname:
			if self.name2:
				return self.surname + ' ' + self.name + ' ' + self.name2 
			return self.surname + ' ' + self.name 

		return self.name

	#Имя файла без пути
	def file_short_name(self):
		str = self.report_file.path
		str = str[str.rfind('/')+1:len(str):1]
		return str


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.username = instance.username
	instance.profile.save()


@receiver(post_delete, sender = Profile)
def profile_post_delete_handler(sender, **kwargs):
	profile = kwargs['instance']

	if profile.report_file:
		if os.path.isfile(profile.report_file.path):
			os.remove(profile.report_file.path)

	if profile.certificate_file:
		if os.path.isfile(profile.certificate_file.path):
			os.remove(profile.certificate_file.path)


@receiver(pre_save, sender = Profile)
def profile_pre_save_handler(sender, **kwargs):
	profile = kwargs['instance']

	if not profile.pk:
		return False

	try:
		old_file = Profile.objects.get(pk=profile.pk).report_file

		if old_file:
			new_file = profile.report_file
			if not old_file==new_file:
				if os.path.isfile(old_file.path):
					os.remove(old_file.path)
	except Profile.DoesNotExist:
		pass


	try:
		old_file = Profile.objects.get(pk=profile.pk).certificate_file

		if old_file:
			new_file = profile.certificate_file
			if not old_file==new_file:
				if os.path.isfile(old_file.path):
					os.remove(old_file.path)
	except Profile.DoesNotExist:
		pass
	