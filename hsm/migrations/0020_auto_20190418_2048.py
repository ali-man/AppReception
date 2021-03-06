# Generated by Django 2.2 on 2019-04-18 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hsm', '0019_auto_20190417_1905'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Оргазинация')),
            ],
            options={
                'verbose_name': 'Организация',
                'verbose_name_plural': 'Организации',
            },
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, verbose_name='Дополнительные услуги')),
                ('price', models.DecimalField(blank=True, decimal_places=0, max_digits=8, null=True, verbose_name='Сумма услуги')),
            ],
            options={
                'verbose_name': 'Дополнительная услуга',
                'verbose_name_plural': 'Дополнительные услуги',
            },
        ),
        migrations.DeleteModel(
            name='DateTest',
        ),
        migrations.RemoveField(
            model_name='typeroom',
            name='price',
        ),
        migrations.AddField(
            model_name='booking',
            name='kpp_date_arrival',
            field=models.DateField(blank=True, null=True, verbose_name='Дата заезда КПП'),
        ),
        migrations.AddField(
            model_name='booking',
            name='kpp_number',
            field=models.CharField(blank=True, max_length=50, verbose_name='КПП №'),
        ),
        migrations.AddField(
            model_name='guest',
            name='email',
            field=models.EmailField(blank=True, max_length=50, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='guest',
            name='phone',
            field=models.CharField(blank=True, max_length=50, verbose_name='Телефон'),
        ),
        migrations.AddField(
            model_name='typeroom',
            name='price_usd',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=8, null=True, verbose_name='Цена комнаты для иностранцев'),
        ),
        migrations.AddField(
            model_name='typeroom',
            name='price_uzs',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=8, null=True, verbose_name='Цена комнаты для граждан РУЗ'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='type_payment',
            field=models.IntegerField(choices=[(1, 'Наличка'), (2, 'Пластик'), (3, 'Перечисление')], default=1, verbose_name='Тип оплаты'),
        ),
        migrations.DeleteModel(
            name='TypePayment',
        ),
    ]
