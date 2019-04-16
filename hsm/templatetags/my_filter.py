import arrow
from django import template

from hsm.models import Booking

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