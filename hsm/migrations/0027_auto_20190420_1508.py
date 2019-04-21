# Generated by Django 2.2 on 2019-04-20 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hsm', '0026_guest_passport'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='alarm',
        ),
        migrations.AddField(
            model_name='booking',
            name='stat',
            field=models.BooleanField(default=True, verbose_name='Состояние брони/объекта'),
        ),
        migrations.AddField(
            model_name='task',
            name='datetime',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата и время напоминания'),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.BooleanField(default=False, verbose_name='Выполнено'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='type_payment',
            field=models.IntegerField(choices=[(0, 'Не известно'), (1, 'Наличка'), (2, 'Пластик'), (3, 'Перечисление'), (4, 'В долларах')], default=0, verbose_name='Тип оплаты'),
        ),
    ]