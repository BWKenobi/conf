# Generated by Django 2.2.16 on 2020-10-26 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileuser', '0007_auto_20201026_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='certificate_number',
            field=models.CharField(blank=True, max_length=30, verbose_name='Номер сертификата'),
        ),
    ]