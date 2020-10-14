import os

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

def make_upload_path(instance, filname):
	return 'profileimage/%s' % filname

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None, blank=True)
	username = models.CharField("Username:", max_length=30, blank=True)

	surname = models.CharField(verbose_name="Фамилия*", max_length=50, blank=True)
	name = models.CharField(verbose_name="Имя*", max_length=30, blank=True)
	name2 = models.CharField(verbose_name="Отчество*", max_length=30, blank=True)
	work_place = models.TextField(verbose_name="Место работы (полностью)*", blank=True)

	registration_date = models.DateField(verbose_name="Дата регистрации", default=timezone.now)
	admin_access= models.BooleanField("Права администратора", default=False)


	def __str__(self):
		if self.user.is_active:
			return self.username
		return self.username + ' (not active)'


	def get_name(self):
		if self.surname:
			if self.name2:
				return self.surname + ' ' + self.name[0] + '.' + self.name2[0]+ '.' 
			return self.surname + ' ' + self.name[0]+ '.' 

		return self.name


	def get_full_name(self):
		if self.surname:
			if self.name2:
				return self.surname + ' ' + self.name + ' ' + self.name2 
			return self.surname + ' ' + self.name 

		return self.name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.username = instance.username
	instance.profile.save()
