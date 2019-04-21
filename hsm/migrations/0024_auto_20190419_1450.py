# Generated by Django 2.2 on 2019-04-19 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hsm', '0023_auto_20190419_1127'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='kpp_date_arrival',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='kpp_number',
        ),
        migrations.AddField(
            model_name='guest',
            name='kpp_date_arrival',
            field=models.CharField(blank=True, max_length=30, verbose_name='Дата заезда КПП'),
        ),
        migrations.AddField(
            model_name='guest',
            name='kpp_number',
            field=models.CharField(blank=True, max_length=50, verbose_name='КПП №'),
        ),
    ]
