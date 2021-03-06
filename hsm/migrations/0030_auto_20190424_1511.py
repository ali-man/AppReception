# Generated by Django 2.2 on 2019-04-24 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hsm', '0029_remove_booking_type_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='early_arrival',
            field=models.BooleanField(default=False, verbose_name='Ранний заезд'),
        ),
        migrations.AddField(
            model_name='booking',
            name='late_departure',
            field=models.BooleanField(default=False, verbose_name='Поздник заезд'),
        ),
    ]
