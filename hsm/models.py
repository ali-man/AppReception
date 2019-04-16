import arrow
from django.contrib import admin
from django.db import models


# Типы номеров
class TypeRoom(models.Model):
    name = models.CharField(verbose_name='Тип комнаты', max_length=50, blank=True)
    price = models.DecimalField(verbose_name='Цена комнаты', max_digits=8, decimal_places=0, null=True, blank=True)

    class Meta:
        verbose_name = 'Тип комнаты'
        verbose_name_plural = 'Типы комнат'

    def __str__(self):
        return self.name


# Имя номеров
class Rooms(models.Model):
    type_room = models.ForeignKey(TypeRoom, verbose_name='Тип комнаты', on_delete=models.CASCADE)
    number_room = models.CharField(verbose_name='Номер комнаты', max_length=50, blank=True)

    class Meta:
        verbose_name = 'Номер комнаты'
        verbose_name_plural = 'Номера комнат'

    def __str__(self):
        return '%s-%s' % (self.type_room.name, self.number_room)


# Метки
class Tag(models.Model):
    name = models.CharField(verbose_name='Тег', max_length=50)

    class Meta:
        verbose_name_plural = 'Теги'
        verbose_name = 'Тег'

    def __str__(self):
        return self.name


# Страны, города
class City(models.Model):
    name = models.CharField(verbose_name="Город", max_length=50)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'

    def __str__(self):
        return self.name


admin.site.register(City)


# Национальность
class Nationality(models.Model):
    name = models.CharField(verbose_name="Национальность", max_length=50)

    class Meta:
        verbose_name = 'Национальность'
        verbose_name_plural = 'Национальности'

    def __str__(self):
        return self.name


admin.site.register(Nationality)


# Данные визы
class Visa(models.Model):
    number = models.CharField(verbose_name="номер", max_length=50)
    visa_type = models.CharField(verbose_name="тип", max_length=50)
    given_date = models.CharField(verbose_name="Дата выдачи", max_length=30)
    expire_date = models.CharField(verbose_name="Дата окончания срока", max_length=30)

    class Meta:
        verbose_name = 'Виза'
        verbose_name_plural = 'Визы'

    def __str__(self):
        return self.number


admin.site.register(Visa)


# Гражданство
class Citeznship(models.Model):
    name = models.CharField(verbose_name='Гражданство', max_length=50)

    class Meta:
        verbose_name = 'Гражданство'
        verbose_name_plural = 'Гражданства'

    def __str__(self):
        return self.name


# Данные гостя
class Guest(models.Model):
    full_name = models.CharField(verbose_name='Ф.И.О', max_length=100, unique=True)
    date_of_birth = models.CharField(verbose_name='Дата рождения', max_length=50, blank=True)
    place_of_birth = models.ForeignKey(City, verbose_name="Место рождение: город", on_delete=models.CASCADE, null=True, blank=True)
    serial_number = models.CharField(verbose_name="Серийный номер паспорта", max_length=50, blank=True)
    given_date = models.CharField(verbose_name="Дата выдачи паспорта", max_length=30, blank=True)
    expire_date = models.CharField(verbose_name="Дата окончания срока паспорта", max_length=30, blank=True)
    give_organization = models.CharField(verbose_name="Кем выдано", max_length=100, blank=True)
    place_of_living = models.CharField(verbose_name="Место проживания", max_length=100, blank=True)
    nationality = models.ForeignKey(Nationality, verbose_name="Национальность", on_delete=models.CASCADE, null=True, blank=True)
    citeznship = models.ForeignKey(Citeznship, verbose_name="Гражданство", on_delete=models.CASCADE, null=True, blank=True)
    visa = models.ForeignKey(Visa, verbose_name="VISA", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.full_name


admin.site.register(Guest)


# Источник откуда поступила бронь
class SourceBooking(models.Model):
    name = models.CharField(verbose_name='Источник бронирования', max_length=50)

    class Meta:
        verbose_name_plural = 'Источники брони'
        verbose_name = 'Источник брони'

    def __str__(self):
        return self.name


admin.site.register(SourceBooking)


# Тип оплаты
class TypePayment(models.Model):
    name = models.CharField(verbose_name='Тип оплаты', max_length=50)

    class Meta:
        verbose_name = 'Тип оплаты'
        verbose_name_plural = 'Типы оплат'

    def __str__(self):
        return self.name


admin.site.register(TypePayment)


# Задачи
class Task(models.Model):
    title = models.CharField(verbose_name='Что сделать', max_length=50, blank=True)
    info = models.TextField(verbose_name='Описание', blank=True)
    alarm = models.IntegerField(verbose_name='Когда выполнить', null=True, blank=True)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title


admin.site.register(Task)


# Информация бронирования
class Booking(models.Model):
    EMPTY = 0
    BOOKING_NOT_PAYMENT = -1
    BOOKING_PAYMENT = 1
    QUEST_ACCOMMODATION_NOT_PAYMENT = -2
    QUEST_ACCOMMODATION_PAYMENT = 2
    EVICTED_ACCOMMODATION = -3
    RESERVE = 3
    GUEST_LEAVE_TODAY = 4
    BLOCKING_ROOM = -4

    STATUS_BOOKING = (
        (EMPTY, 'Пусто'),
        (BOOKING_NOT_PAYMENT, 'Бронь без оплаты'),
        (BOOKING_PAYMENT, 'Бронь с предоплатой'),
        (QUEST_ACCOMMODATION_NOT_PAYMENT, 'Размещение гостя с долгом'),
        (QUEST_ACCOMMODATION_PAYMENT, 'Размещение гостя с оплатой'),
        (EVICTED_ACCOMMODATION, 'Выселенное размещение'),
        (RESERVE, 'Резерв'),
        (GUEST_LEAVE_TODAY, 'Гости сегодня выезжают'),
        (BLOCKING_ROOM, 'Блокировка номера'),
    )

    guest = models.ManyToManyField(Guest, verbose_name='Проживающие гости', blank=True)
    room = models.ForeignKey(Rooms, verbose_name='Номер остановки', on_delete=models.CASCADE, null=True, blank=True)
    date_of_arrival = models.IntegerField(verbose_name='Дата заезда в Timestamp', default=0)
    date_of_arrival_time = models.CharField(verbose_name='Время заезда', max_length=10, blank=True)
    date_of_departure = models.IntegerField(verbose_name='Дата выезда в Timestamp', default=0)
    date_of_departure_time = models.CharField(verbose_name='Время выезда', max_length=10, blank=True)
    date_arrival = models.DateTimeField(verbose_name='Дата и время заезда', null=True, blank=True)
    date_departure = models.DateTimeField(verbose_name='Дата и время выезда', null=True, blank=True)
    price_per_night = models.DecimalField(verbose_name='Цена за ночь', max_digits=10, decimal_places=0)
    price_for_all_time = models.DecimalField(verbose_name='Цена за неделю', max_digits=10, decimal_places=0)
    type_payment = models.ForeignKey(TypePayment, verbose_name='Тип оплаты', on_delete=models.CASCADE, null=True,
                                     blank=True)
    source_of_booking = models.ForeignKey(SourceBooking, verbose_name='Источник бронирования', on_delete=models.CASCADE,
                                          null=True, blank=True)
    number_source_booking = models.CharField(verbose_name='Номер брони источника', max_length=50, blank=True)
    status_booking = models.IntegerField(verbose_name='Статус брони', choices=STATUS_BOOKING, default=EMPTY)
    admin_comment = models.TextField(verbose_name='Комментарий администратора', blank=True)
    customer_wishes = models.TextField(verbose_name='Пожелания гостя', blank=True)
    task = models.ForeignKey(Task, verbose_name='Задачи', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'

    def __str__(self):
        date_format = '%d-%m-%Y'
        date_arrival = arrow.get(self.date_of_arrival).datetime.strftime(date_format)
        date_departure = arrow.get(self.date_of_departure).datetime.strftime(date_format)

        return F'Дата заезда: {date_arrival} Дата выезда: {date_departure} - {self.room}'


admin.site.register(Booking)


class DateTest(models.Model):
    name = models.CharField(verbose_name='Тестовое название', max_length=50, blank=True)
    date_arrival = models.DateTimeField(verbose_name='Дата заезда')
    date_departure = models.DateTimeField(verbose_name='Дата выезда')

    class Meta:
        verbose_name = 'Тестовый'
        verbose_name_plural = 'Тестовые'

    def __str__(self):
        return F'{self.name} {self.date_arrival.date()} {self.date_arrival.time()} --- {self.date_departure.date()} {self.date_departure.time()}'


admin.site.register(DateTest)