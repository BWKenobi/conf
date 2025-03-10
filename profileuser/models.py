import os
from pytils import translit

from django.utils import timezone
from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from sections.models import Section

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
	SPEAKER_TYPE = (
		('1', 'Выступление с докладом'),
		('2', 'Участие без доклада'),
	)
	
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None, blank=True)
	username = models.CharField("Username:", max_length=30, blank=True)

	surname = models.CharField(verbose_name="Фамилия*", max_length=50, blank=True)
	name = models.CharField(verbose_name="Имя*", max_length=30, blank=True)
	name2 = models.CharField(verbose_name="Отчество", max_length=30, blank=True)
	phone = models.CharField(verbose_name="Телефон*", max_length=30, blank=True)
	work_place = models.CharField(verbose_name="Название организации*", max_length=250, blank=True)
	work_part = models.CharField(verbose_name="Название отдела (факультет, кафедра)", max_length=250, blank=True)
	position = models.CharField(verbose_name="Занимаемая должность", max_length=100, blank=True)
	degree = models.CharField(verbose_name="Ученая степень, ученое звание", max_length=100, blank=True)

	section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True, default=None, blank=True)

	certificate_num = models.CharField(verbose_name="Номер сертификата", max_length=30, blank=True)
	certificate_file = models.FileField(verbose_name='Сертификат', blank=True, null=True, upload_to = make_certificate_path)

	speaker= models.CharField("Форма участия", max_length=1, choices=SPEAKER_TYPE, default='2')
	report_name = models.CharField(verbose_name="Тема доклада", max_length=250, blank=True)
	report_file = models.FileField(verbose_name='Файл научной статьи (при наличии)', blank=True, null=True, upload_to = make_upload_path)

	registration_date = models.DateField(verbose_name="Дата регистрации", default=timezone.now)
	admin_access= models.BooleanField("Права администратора", default=False)
	moderator_access= models.BooleanField("Права модератора", default=False)
	message_accecc = models.BooleanField("Права рассылки оповещений", default=False)

	org_accecc = models.BooleanField("Права орг.комитета", default=False)


	def __str__(self):
		if self.user.is_active:
			return self.username
		return self.username + ' (not active)'


	def sex(self):
		sex = False
		if not self.name2:
			return sex
		if self.name2[-1] =='ч' or self.name2[-1] == 'Ч':
			sex = True
		return sex


	def sex_valid(self):
		sex_valid = False
		if not self.name2:
			return sex_valid
		if self.name2[-1] =='ч' or self.name2[-1] == 'Ч' or self.name2[-1] =='а' or self.name2[-1] == 'А':
			sex_valid = True
		return sex_valid


	def get_name(self):
		admin = ''
		if self.admin_access:
			admin = ' (Администратор)'
		elif self.org_accecc:
			admin = ' (Орг.комитет)'
		if self.surname:
			if self.name2:
				return self.surname + ' ' + self.name[0] + '.' + self.name2[0]+ '.' + admin
			return self.surname + ' ' + self.name[0]+ '.'  + admin

		return self.name + admin


	def get_file_name(self):
		if self.surname:
			if self.name2:
				return self.surname + ' ' + self.name[0] + '.' + self.name2[0]+ '.'
			return self.surname + ' ' + self.name[0]+ '.'

		return self.name


	def get_io_name(self):
		if self.name2:
			return self.name + ' ' + self.name2 
		return self.name 


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

	#Статус
	def status(self):
		if self.speaker:
			return 'Докладчик'
		return 'Участник'
		

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
	