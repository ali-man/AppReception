from django.db import models


class TypeRoom(models.Model):
    name = models.CharField(verbose_name='Тип комнаты', max_length=50, blank=True)
    price = models.DecimalField(verbose_name='Цена комнаты', max_digits=8, decimal_places=0, null=True, blank=True)

    class Meta:
        verbose_name = 'Тип комнаты'
        verbose_name_plural = 'Типы комнат'

    def __str__(self):
        return self.name


class Rooms(models.Model):
    type_room = models.ForeignKey(TypeRoom, verbose_name='Тип комнаты', on_delete=models.CASCADE)
    number_room = models.IntegerField(verbose_name='Номер комнаты', null=True, blank=True)

    class Meta:
        verbose_name = 'Номер комнаты'
        verbose_name_plural = 'Номера комнат'

    def __str__(self):
        return '%s' % self.number_room
