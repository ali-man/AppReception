# Generated by Django 2.2 on 2019-04-29 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hsm', '0038_auto_20190426_0401'),
    ]

    operations = [
        migrations.AddField(
            model_name='rooms',
            name='close',
            field=models.BooleanField(default=False, verbose_name='Закрыть номер'),
        ),
    ]
