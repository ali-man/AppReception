import datetime

from django.shortcuts import redirect, render
from django.views.generic.base import View

from hsm.models import TypeRoom, Booking


def date_in_to_out(date_in, date_out):
    # 24-04-2019
    if date_in and date_out is not None:
        da = list(map(int, date_in.split('-')))
        dd = list(map(int, date_out.split('-')))
        date_in = datetime.date(da[2], da[1], da[0])
        date_out = datetime.date(dd[2], dd[1], dd[0])
        days = (date_out - date_in).days + 1
    else:
        days = 15
        today = datetime.datetime.now().date()
        date_in = today + datetime.timedelta(days=-2)
        date_out = today + datetime.timedelta(days=13)

    return days, date_in, date_out


class ChessViews(View):
    @staticmethod
    def get(request):
        if request.user.is_anonymous:
            return redirect('/login')

        days, date_in, date_out = date_in_to_out(request.GET.get('date_in', None), request.GET.get('date_out', None))
        type_rooms = TypeRoom.objects.all()
        bookings = Booking.objects.exclude(stat=False, status_booking=-3)

        db = {}
        today = datetime.datetime.now().date()
        dates = [date_in + datetime.timedelta(days=day) for day in range(days)]

        for tr in type_rooms:
            db[tr.name] = {}
            for r in tr.rooms_set.filter(close=False):
                db[tr.name][r.__str__()] = {}
                for day in range(days):
                    date = date_in + datetime.timedelta(days=day)
                    for b in bookings:
                        if str(b.room) == r.__str__() and b.date_arrival.date() <= date < b.date_departure.date():
                            db[tr.name][r.__str__()][date] = [b.id, b.status_booking]
                    if date not in db[tr.name][r.__str__()]:
                        db[tr.name][r.__str__()][date] = ['freeday', '']

        free_rooms = []
        for tr_k, tr_v in db.items():
            for r_k, r_v in tr_v.items():
                freedays = [d_v for d_k, d_v in r_v.items() if d_v == ['freeday', '']]
                if len(freedays) == days:
                    free_rooms.append(r_k)

        context = {
            'db': db,
            'today': today,
            'dates': dates,
            'free_rooms': free_rooms,
            'date_in': date_in,
            'date_out': date_out,
            'days': days
        }
        return render(request, 'chess.html', context)

    @staticmethod
    def post(request):
        pass
