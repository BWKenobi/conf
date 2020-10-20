# Generated by Django 2.2.16 on 2020-10-17 16:37

from django.db import migrations, models
import profileuser.models


class Migration(migrations.Migration):

    dependencies = [
        ('profileuser', '0002_auto_20201010_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='report_file',
            field=models.FileField(blank=True, null=True, upload_to=profileuser.models.make_upload_path, verbose_name='Файл доклада'),
        ),
        migrations.AddField(
            model_name='profile',
            name='report_name',
            field=models.CharField(blank=True, max_length=250, verbose_name='Тема доклада*'),
        ),
        migrations.AddField(
            model_name='profile',
            name='speaker',
            field=models.BooleanField(default=False, verbose_name='Докладчик'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='work_place',
            field=models.TextField(blank=True, verbose_name='Место работы (полностью)*'),
        ),
    ]