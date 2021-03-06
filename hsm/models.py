import arrow
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models


# Типы номеров
class TypeRoom(models.Model):
    name = models.CharField(verbose_name='Тип комнаты', max_length=50, blank=True)
    price_uzs = models.DecimalField(verbose_name='Цена комнаты для граждан РУЗ', max_digits=8, decimal_places=0,
                                    null=True, blank=True)
    price_usd = models.DecimalField(verbose_name='Цена комнаты для иностранцев', max_digits=8, decimal_places=0,
                                    null=True, blank=True)

    class Meta:
        verbose_name = 'Тип комнаты'
        verbose_name_plural = 'Типы комнат'

    def __str__(self):
        return self.name


# Имя номеров
class Rooms(models.Model):
    type_room = models.ForeignKey(TypeRoom, verbose_name='Тип комнаты', on_delete=models.CASCADE)
    number_room = models.CharField(verbose_name='Номер комнаты', max_length=50, blank=True)
    close = models.BooleanField(verbose_name='Закрыть номер', default=False)
    clean = models.BooleanField(verbose_name='Статус номера', default=True)

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
    phone = models.CharField(verbose_name='Телефон', max_length=50, blank=True)
    email = models.EmailField(verbose_name='Email', max_length=50, blank=True)
    passport = models.BooleanField(verbose_name='Паспорт в наличии', default=True)
    date_of_birth = models.CharField(verbose_name='Дата рождения', max_length=50, blank=True)
    place_of_birth = models.ForeignKey(City, verbose_name="Место рождение: город", on_delete=models.CASCADE, null=True,
                                       blank=True)
    serial_number = models.CharField(verbose_name="Серийный номер паспорта", max_length=50, blank=True)
    given_date = models.CharField(verbose_name="Дата выдачи паспорта", max_length=30, blank=True)
    expire_date = models.CharField(verbose_name="Дата окончания срока паспорта", max_length=30, blank=True)
    give_organization = models.CharField(verbose_name="Кем выдано", max_length=100, blank=True)
    place_of_living = models.CharField(verbose_name="Место проживания", max_length=100, blank=True)
    nationality = models.ForeignKey(Nationality, verbose_name="Национальность", on_delete=models.CASCADE, null=True,
                                    blank=True)
    citeznship = models.ForeignKey(Citeznship, verbose_name="Гражданство", on_delete=models.CASCADE, null=True,
                                   blank=True)
    kpp_number = models.CharField(verbose_name='КПП №', max_length=50, blank=True)
    kpp_date_arrival = models.CharField(verbose_name='Дата заезда КПП', max_length=30, blank=True)
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


# Задачи
class Task(models.Model):
    title = models.CharField(verbose_name='Что сделать', max_length=50, blank=True)
    info = models.TextField(verbose_name='Описание', blank=True)
    # alarm = models.IntegerField(verbose_name='Когда выполнить', null=True, blank=True)
    datetime = models.DateTimeField(verbose_name='Дата и время напоминания', null=True, blank=True)
    status = models.BooleanField(verbose_name='Выполнено', default=False)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title


admin.site.register(Task)


class Organization(models.Model):
    name = models.CharField(verbose_name='Оргазинация', max_length=100, blank=True)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name


admin.site.register(Organization)


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

    A = 0
    B = 1
    C = 2
    D = 3
    E = 4
    TYPE_PAYMENT = (
        (A, 'Не известно'),
        (B, 'Наличка'),
        (C, 'Пластик'),
        (D, 'Перечисление'),
        (E, 'В долларах')
    )

    date_arrival = models.DateTimeField(verbose_name='Дата и время заезда', null=True, blank=True)
    early_arrival = models.BooleanField(verbose_name='Ранний заезд', default=False)
    date_departure = models.DateTimeField(verbose_name='Дата и время выезда', null=True, blank=True)
    late_departure = models.BooleanField(verbose_name='Поздник заезд', default=False)
    price_per_night = models.DecimalField(verbose_name='Цена за ночь', max_digits=10, decimal_places=0, default=0)
    price_for_all_time = models.DecimalField(verbose_name='Цена за всё время', max_digits=10, decimal_places=0,
                                             default=0)
    payment_nal = models.DecimalField(verbose_name='Сумма - налом', max_digits=10, decimal_places=0, default=0)
    payment_bez_nal = models.DecimalField(verbose_name='Сумма - перечисление', max_digits=10, decimal_places=0,
                                          default=0)
    payment_terminal = models.DecimalField(verbose_name='Сумма - терминал', max_digits=10, decimal_places=0, default=0)
    payment_usd = models.DecimalField(verbose_name='Сумма - в долларах', max_digits=10, decimal_places=0, default=0)
    paid = models.DecimalField(verbose_name='Оплачено', max_digits=10, decimal_places=0, default=0)
    left_to_pay = models.DecimalField(verbose_name='Осталось оплатить', max_digits=10, decimal_places=0, default=0)
    days = models.FloatField(verbose_name='Суток', null=True, blank=True)
    status_booking = models.IntegerField(verbose_name='Статус брони', choices=STATUS_BOOKING, default=EMPTY)

    user = models.ForeignKey(User, verbose_name='Администратор', on_delete=models.CASCADE, null=True, blank=True)
    guest = models.ManyToManyField(Guest, verbose_name='Проживающие гости', blank=True)
    organization = models.ForeignKey(Organization, verbose_name='Организация', on_delete=models.CASCADE, null=True,
                                     blank=True)
    room = models.ForeignKey(Rooms, verbose_name='Номер остановки', on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey(Task, verbose_name='Задачи', on_delete=models.CASCADE, null=True, blank=True)
    source_of_booking = models.ForeignKey(SourceBooking, verbose_name='Источник бронирования', on_delete=models.CASCADE,
                                          null=True, blank=True)
    number_source_booking = models.CharField(verbose_name='Номер брони источника', max_length=50, blank=True)
    admin_comment = models.TextField(verbose_name='Комментарий администратора', blank=True)
    customer_wishes = models.TextField(verbose_name='Пожелания гостя', blank=True)

    stat = models.BooleanField(verbose_name='Состояние брони/объекта', default=True)

    class Meta:
        verbose_name = 'Бронь'
        verbose_name_plural = 'Брони'

    def save(self, *args, **kwargs):
        self.days = (self.date_departure.date() - self.date_arrival.date()).days
        if self.early_arrival:
            self.days += 0.5
        if self.late_departure:
            self.days += 0.5
        if self.price_per_night == 0:
            self.price_per_night = self.room.type_room.price_uzs
        self.price_for_all_time = int(int(self.price_per_night) * float(self.days))
        if self.payment_usd == 0:
            all_payment = self.payment_nal + self.payment_bez_nal + self.payment_terminal
            left_to_pay = self.price_for_all_time - all_payment
            self.paid = all_payment
            self.left_to_pay = left_to_pay
        else:
            self.paid = self.payment_usd
            self.left_to_pay = self.price_for_all_time - self.payment_usd

        super(Booking, self).save(*args, **kwargs)

    def __str__(self):
        return F'Дата заезда: {self.date_arrival} Дата выезда: {self.date_departure} - {self.room}'


class Checks(models.Model):
    check_number = models.IntegerField(verbose_name='Номер счёта')
    booking = models.ForeignKey(Booking, verbose_name='Бронь', on_delete=models.CASCADE)
    kassir = models.ForeignKey(User, verbose_name='Кассир', on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(verbose_name='Дата и время создания чека', auto_now_add=True)

    class Meta:
        verbose_name = 'Чек'
        verbose_name_plural = 'Чеки'

    def __str__(self):
        return '%s' % self.check_number


admin.site.register(Checks)


class Services(models.Model):
    booking = models.OneToOneField(Booking, verbose_name='Бронь', null=True, blank=True, on_delete=models.CASCADE)
    paid = models.DecimalField(verbose_name='Оплачено', max_digits=11, decimal_places=0, default=0)

    class Meta:
        verbose_name = 'Дополнительная услуга'
        verbose_name_plural = 'Дополнительные услуги'

    def get_price_all(self):
        return sum(i.price for i in self.paymentservices_set.all())

    def get_debt(self):
        return self.get_price_all() - self.paid

    # def save(self, *args, **kwargs):
    #     super(Services, self).save(*args, **kwargs)

    def __str__(self):
        return '%s' % self.id


class PaymentServices(models.Model):
    service = models.ForeignKey(Services, verbose_name='ID услуги', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Услуга', max_length=100, blank=True)
    price = models.DecimalField(verbose_name='Сумма услуги', max_digits=8, decimal_places=0, null=True, blank=True)

    class Meta:
        verbose_name = 'Доп. услуга'
        verbose_name_plural = 'Доп. услуги'

    def __str__(self):
        return '%s %s' % (self.name, self.price)
