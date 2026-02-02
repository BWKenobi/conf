import os
from pytils import translit

from django.utils import timezone
from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver


class Answer(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None, blank=True)

	answer_1 = models.TextField(verbose_name='Какая информация была наиболее интересной и полезной для  Вас?', blank=True)
	answer_2 = models.TextField(verbose_name='Какие темы могут быть еще Вам интересны?', blank=True)
	answer_3 = models.TextField(verbose_name='Какие доклады и мастер-классы Вы могли бы предложить к проведению?', blank=True)

	done = models.BooleanField("Анкета сохранена", default=False)

	class Meta:
		ordering = ['user__profile__surname']
		verbose_name='Анкета'
		verbose_name_plural='Анкеты'

	def __str__(self):
		return str(self.user.profile)
