# Generated by Django 2.2.16 on 2020-10-26 08:32

from django.db import migrations
import profileuser.models
import utf8field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('profileuser', '0005_auto_20201026_0058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='certificate_file',
            field=utf8field.fields.UTF8FileField(blank=True, null=True, upload_to=profileuser.models.make_certificate_path, verbose_name='Сертификат'),
        ),
    ]