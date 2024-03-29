# Generated by Django 2.2.19 on 2023-03-18 15:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import profileuser.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=30, verbose_name='Username:')),
                ('surname', models.CharField(blank=True, max_length=50, verbose_name='Фамилия*')),
                ('name', models.CharField(blank=True, max_length=30, verbose_name='Имя*')),
                ('name2', models.CharField(blank=True, max_length=30, verbose_name='Отчество')),
                ('work_place', models.CharField(blank=True, max_length=250, verbose_name='Название организации*')),
                ('position', models.CharField(blank=True, max_length=100, verbose_name='Занимаемая должность')),
                ('certificate_num', models.CharField(blank=True, max_length=30, verbose_name='Номер сертификата')),
                ('certificate_file', models.FileField(blank=True, null=True, upload_to=profileuser.models.make_certificate_path, verbose_name='Сертификат')),
                ('speaker', models.CharField(choices=[('1', 'Докладчик'), ('2', 'Участник')], default='3', max_length=1, verbose_name='Форма участия')),
                ('registration_date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата регистрации')),
                ('admin_access', models.BooleanField(default=False, verbose_name='Права администратора')),
                ('moderator_access', models.BooleanField(default=False, verbose_name='Права модератора')),
                ('message_accecc', models.BooleanField(default=False, verbose_name='Права рассылки оповещений')),
                ('user', models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
