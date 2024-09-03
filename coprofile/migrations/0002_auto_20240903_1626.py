# Generated by Django 2.2.19 on 2024-09-03 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coprofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coprofile',
            name='speaker',
            field=models.CharField(choices=[('1', 'Выступление с докладом (очно)'), ('4', 'Выступление с докладом (он-лайн)'), ('2', 'Публикация статьи'), ('3', 'Участие без доклада')], default='3', max_length=1, verbose_name='Форма участия'),
        ),
    ]
