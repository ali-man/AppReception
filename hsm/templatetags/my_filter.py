import datetime

import arrow
from django import template

from hsm.models import Booking
from hsm.ru_number_to_text import num2text

register = template.Library()


@register.filter(name='create_range')
def create_range(value, start_index=0):
    return range(start_index, value + start_index)


@register.filter(name='day')
def date_day(value):
    return value[0].split('-')[0]


@register.filter(name='weekday')
def date_weekday(value):
    return value[0].split(', ')[-1]


@register.filter(name='today')
def date_today(value):
    return " ".join(value.split(', ')[0].split('-')[1:])


def to_timestamp(_date):
    # _date == '14-04-2019, Вс'
    # print(_date)
    list_date = _date.split(', ')[0].split('-')  # ['14', '04', '2019']
    date = [int(i) for i in list_date]  # [14, 4, 2019]
    date_to_timestamp = arrow.get(date[2], date[1], date[0]).timestamp  # 15789900 TIMESTAMP
    return date_to_timestamp


@register.filter(name='checking_date')
def checking_date(timestamp, room):
    print(timestamp)
    bookings_all = Booking.objects.all()
    bookings = bookings_all.filter(room=room, date_of_arrival__lte=timestamp, date_of_departure__gte=timestamp)
    result = None
    for i in bookings:
        print(F'{i.room} == {room}')
        if i.date_of_arrival <= timestamp <= i.date_of_departure and i.room == room:
            result = True
        else:
            result = False
    return result


@register.filter(name='info_booking')
def info_booking(timestamp, room):
    print(room)
    bookings = Booking.objects.filter(room=room, date_of_arrival__lte=timestamp, date_of_departure__gte=timestamp)
    result = None
    for i in bookings:
        if i.date_of_arrival <= timestamp <= i.date_of_departure and i.room == room:
            result = i.id
    return result


@register.filter(name='date_full_to_date')
def date_full_to_date(date_full):
    return date_full.strftime("%d")


@register.filter(name='status_booking')
def status_booking(status):
    return {
        -1: 'Бронь без оплаты',
        1: 'Бронь с предоплатой',
        -2: 'Размещение гостя с долгом',
        2: 'Размещение гостя с оплатой',
        -3: 'Выселенное размещение',
        3: 'Резерв',
        4: 'Гости сегодня выезжают',
        -4: 'Блокировка номера',
    }[status]


@register.filter(name='status_booking_print')
def status_booking_print(status):
    return {
        -1: 'Бронь',
        1: 'Бронь',
        -2: 'Проживает',
        2: 'Проживает',
        -3: 'Выселен',
        3: 'Резерв',
        4: 'Проживает',
    }[status]


@register.filter(name='tester')
def tester(req):
    print(type(req))
    print(req)


@register.filter(name='type_payment')
def type_payment(val):
    return {
        0: 'Неизвестно',
        1: 'Наличка',
        2: 'Пластик',
        3: 'Без нал (Перечисление)',
        4: 'В долларах'
    }[val]


@register.filter(name='checking_booking')
def checking_booking(date, room):
    booking = Booking.objects.filter(stat=True, date_arrival__date__lte=date, date_departure__date__gte=date, room=room)
    if str(booking) == '<QuerySet []>':
        return False
    else:
        return True


@register.filter(name='week_day')
def week_day(w):
    return {
        0: 'Пн',
        1: 'Вт',
        2: 'Ср',
        3: 'Чт',
        4: 'Пт',
        5: 'Сб',
        6: 'Вс'
    }[w]


@register.filter(name='today_booking')
def today_booking(room, date):
    b = Booking.objects.filter(stat=True, date_arrival__date__lte=date, date_departure__date__gte=date).exclude(status_booking=-3).order_by('-id')
    bookings = b.filter(room=room)
    for i in bookings:
        if i.date_departure.date() == date:
            return F'status{i.status_booking} {i.id} today-departure'
        elif i.date_arrival.date() == date:
            return F'status{i.status_booking} {i.id} today-arrival'
        elif i.date_arrival.date() <= date <= i.date_departure.date():
            return F'status{i.status_booking} {i.id}'
        else:
            return 'freeday'

    if room.clean:
        return 'freeday'
    else:
        return 'freeday dirty'


@register.filter(name='organization')
def organization(org):
    if org is None:
        return 'Индивидуал'
    else:
        return org


@register.filter(name='type_room')
def type_room(room):
    return room.split(' ')[0]


@register.filter(name='number_to_str')
def number_to_str(num):
    return num2text(int(num))


@register.filter(name='divide_price')
def divide_price(price, guests):
    quantity = len(list(guests))
    result = price / quantity
    return result