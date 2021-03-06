# Generated by Django 2.2 on 2019-04-24 10:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hsm', '0033_auto_20190424_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ownservicesbooking',
            name='booking',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='osb', to='hsm.Booking', verbose_name='ID брони'),
        ),
        migrations.AlterField(
            model_name='servicesbooking',
            name='booking',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sb', to='hsm.Booking', verbose_name='ID брони'),
        ),
        migrations.AlterField(
            model_name='servicesbooking',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sbs', to='hsm.Services', verbose_name='Доп. услуга'),
        ),
    ]
