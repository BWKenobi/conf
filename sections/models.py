import os
from pytils import translit

from django.utils import timezone
from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver


class Section(models.Model):
	name = models.CharField(verbose_name="Название секции", max_length=100)
	count = models.DecimalField(verbose_name="Количество участников", max_digits=2, decimal_places=0, default=1, blank=False)

	class Meta:
		ordering = ['name']
		verbose_name='Секция'
		verbose_name_plural='Секции'

	def __str__(self):
		return self.name
