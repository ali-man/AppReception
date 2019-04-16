# Generated by Django 2.2 on 2019-04-16 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hsm', '0013_auto_20190414_2002'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, verbose_name='Тестовое название')),
                ('date_arrival', models.DateTimeField(verbose_name='Дата заезда')),
                ('date_departure', models.DateTimeField(verbose_name='Дата выезда')),
            ],
            options={
                'verbose_name': 'Тестовый',
                'verbose_name_plural': 'Тестовые',
            },
        ),
    ]