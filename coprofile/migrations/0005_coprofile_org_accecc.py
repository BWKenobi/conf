# Generated by Django 2.2.19 on 2025-02-05 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coprofile', '0004_coprofile_section'),
    ]

    operations = [
        migrations.AddField(
            model_name='coprofile',
            name='org_accecc',
            field=models.BooleanField(default=False, verbose_name='Права орг.комитета'),
        ),
    ]
