# Generated by Django 2.2.19 on 2022-09-10 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coprofile', '0002_auto_20220910_0116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coprofile',
            name='speaker',
            field=models.CharField(choices=[('1', 'Выступление с докладом'), ('2', 'Публикация статьи'), ('3', 'Участие без доклада')], default='3', max_length=1, verbose_name='Форма участия'),
        ),
    ]
