import datetime
import calendar

import arrow
from django.shortcuts import render, redirect
from django.views.generic.base import View

from hsm.booking import guest_register, request_processing, visa_register, booking_register
from hsm.forms import GuestForm
from hsm.models import TypeRoom, SourceBooking, Booking, Guest


def main_page(request):
    return redirect('chess/')


def int_to_str(x):
    return {
        0: 'Пн',
        1: 'Вт',
        2: 'Ср',
        3: 'Чт',
        4: 'Пт',
        5: 'Сб',
        6: 'Вс'
    }[x]


def change_date_num(x):
    # x == '03 05 2019'
    list_x = x.split(' ')
    result = [int(i) for i in list_x]
    # result[0] = result[0][1] if result[0][0] == '0' else result[0]
    # result[1] = result[1][1] if result[1][0] == '0' else result[1]
    return " ".join(result)


def date_list():
    date_format = "%d-%m-%Y"
    today = datetime.datetime.now()

    dates = {
        'full_date': [],
        'timestamp': [],
        'today': F'{today.strftime(date_format)}, {int_to_str(today.weekday())}'
    }
    for i in range(-3, 12):
        date = today + datetime.timedelta(days=i)
        timestamp_format = '%Y, %m, %d'
        dt = [int(i) for i in date.strftime(timestamp_format).split(', ')]
        ts = arrow.get(dt[0], dt[1], dt[2]).timestamp
        weekday_num = date.weekday()
        dates['full_date'].append([
            F'{date.strftime(date_format)}, {int_to_str(weekday_num)}',
            ts
        ])
    print(dates['full_date'])
    return dates


class ChessViews(View):
    @staticmethod
    def get(request):
        type_rooms = TypeRoom.objects.all()
        dates = date_list()
        bookings = Booking.objects.all()

        date = {
            'full_date': dates['full_date'],
            'today': dates['today'],
            # 'bookings':
        }

        context = {
            'date': date,
            'type_rooms': type_rooms,
        }
        return render(request, 'chess.html', context=context)

    @staticmethod
    def post(request):
        pass


class BookingViews(View):
    @staticmethod
    def get(request):
        source_booking = SourceBooking.objects.all()
        type_rooms = TypeRoom.objects.all()
        price = 'Надо продумать'
        arrival = datetime.datetime.now().strftime("%d-%m-%Y")
        departure = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d-%m-%Y")
        sb = Booking.STATUS_BOOKING
        status_booking = (sb[1], sb[2], sb[3], sb[4], sb[6])
        form_guest = GuestForm()
        context = {
            'source_booking': source_booking,
            'type_rooms': type_rooms,
            'price': price,
            'arrival': arrival,
            'departure': departure,
            'sb': sb,
            'status_booking': status_booking,
            'form_guest': form_guest
        }

        return render(request, 'booking.html', context=context)

    @staticmethod
    def post(request):
        # print(request.POST)
        req = request_processing(request.POST)
        visa = visa_register(req['visa'])
        print(visa)
        print(req['guest'])
        guest = guest_register(visa, req['guest'])
        # print(guest)
        booking_register(guest, req['booking'])

        return redirect('/')
