# Generated by Django 2.2 on 2019-04-10 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hsm', '0005_auto_20190410_1419'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name': 'Страна', 'verbose_name_plural': 'Страны'},
        ),
        migrations.AlterField(
            model_name='task',
            name='info',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
    ]