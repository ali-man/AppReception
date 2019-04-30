import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic.base import View

from hsm.booking import guest_register, request_processing, visa_register, booking_register
from hsm.forms import GuestForm, EditBookingForm, StatusForm, OrganizationForm
from hsm.functions import int_to_str
from hsm.models import TypeRoom, SourceBooking, Booking, Guest, Task, Organization


class HomeViews(View):
    @staticmethod
    def get(request):
        filter_date = request.GET.get('filter_date', None)
        if filter_date is None:
            date = datetime.datetime.now().date()
        else:
            # 24-04-2019
            sort = list(map(int, filter_date.split('-')))
            date = datetime.date(sort[2], sort[1], sort[0])
        bookings = Booking.objects.filter(stat=True)
        today_departure = len(bookings.filter(date_departure__date=date))
        today_arrival = len(bookings.filter(date_arrival__date=date))
        today_resident = bookings.filter(date_arrival__date__lte=date, date_departure__date__gte=date).exclude(status_booking=-3).order_by('-id')
        today_booking = len(today_resident)
        today_free = settings.ROOMS_QUANTITY - today_booking
        # Гражданины РУЗ
        guests_ruz = len(today_resident.filter(guest__citeznship_id=settings.CITEZNSHIP_RUZ))
        # Гражданины Рф
        guests_rf = len(today_resident.filter(guest__citeznship_id=settings.CITEZNSHIP_RF))
        # Гражданины Ин
        guests_in = len(today_resident.exclude(guest__citeznship_id=settings.CITEZNSHIP_RUZ).exclude(guest__citeznship_id=settings.CITEZNSHIP_RF))
        type_rooms = TypeRoom.objects.all()

        return render(request, 'home.html', locals())

    @staticmethod
    def post(request):
        pass


class ChessViews(View):
    # @login_required(login_url='/login')
    @staticmethod
    def get(request, _date=None):
        today = datetime.datetime.now()
        if request.user.is_anonymous:
            return redirect('/login/')
        booking_all = Booking.objects.filter(stat=True)
        type_rooms = TypeRoom.objects.all()
        logic = True
        db = {}
        dates = {
            'date_days': [],
            'date_weekdays': []
        }
        if _date is None:
            for n in range(-2, 13):
                date_full = today + datetime.timedelta(days=n)
                date = date_full.date()
                dates['date_days'].append(date.day)
                dates['date_weekdays'].append(int_to_str(date.weekday()))

            for i in type_rooms:
                db[i.name] = {}
                for j in i.rooms_set.all():
                    db[i.name][j.__str__()] = {}
                    for n in range(-2, 13):
                        date_full = today + datetime.timedelta(days=n)
                        date = date_full.date()
                        try:
                            b = booking_all.get(date_arrival__date__lte=date, date_departure__date__gte=date,
                                                room=j)
                            # if (b.date_arrival.date() <= date <= b.date_departure.date()) and (
                            #         str(b.room) == j.__str__()):
                            db[i.name][j.__str__()][date] = b
                        except Booking.DoesNotExist:
                            db[i.name][j.__str__()][date] = ['f', i.price_uzs, i.price_usd]
                        except Booking.MultipleObjectsReturned:
                            # TODO: две брони на один день (дело в дате)
                            if logic:
                                print('true')
                                b = booking_all.filter(date_arrival__date__lte=date, date_departure__date__gte=date, room=j)[1]
                                logic = False
                            else:
                                print('false')
                                b = booking_all.filter(date_arrival__date__lte=date, date_departure__date__gte=date, room=j)[0]
                                logic = True
                            db[i.name][j.__str__()][date] = b # [date] в этом дело

        return render(request, 'chess.html', {'alls': db, 'dates': dates, 'today': today})

    @staticmethod
    def post(request):
        pass


# @login_required(redirect_field_name='/login')
class BookingViews(View):
    @staticmethod
    def get(request: object, data: object = None) -> object:
        print(request)
        print(data)
        if request.user.is_authenticated:
            source_booking = SourceBooking.objects.all()
            type_rooms = TypeRoom.objects.all()
            # TODO: Подумать price
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
        else:
            return redirect('/login/')

    @staticmethod
    def post(request):
        req = request_processing(request.POST)
        if req['visa']['number'] == '':
            guest = guest_register(req['guest'])
        else:
            visa = visa_register(req['visa'])
            guest = guest_register(req['guest'], visa)
        booking_register(guest, req['booking'])

        return redirect('/')


class EditBookingViews(View):
    @staticmethod
    def get(request, id):
        if request.user.is_authenticated:
            booking = Booking.objects.get(id=id)
            form = EditBookingForm(instance=booking)
            return render(request, 'booking/edit.html', locals())
        else:
            return redirect('/')

    @staticmethod
    def post(request, id):
        save = request.POST['save']
        if request.user.is_authenticated:
            booking = Booking.objects.get(id=id)
            form = EditBookingForm(request.POST, instance=booking)
            if form.is_valid():
                form.save()
                if save == 'continue':
                    return redirect('/booking/edit-' + str(id))
                else:
                    return redirect('/')
            return redirect('/booking/edit-' + str(id))
        else:
            return redirect('/')


class DetailBookingViews(View):
    @staticmethod
    def get(request: object, id: object) -> object:
        booking = Booking.objects.get(id=id)
        return render(request, 'booking/detail.html', locals())

    @staticmethod
    def post(request):
        pass


class StatusBookingViews(View):
    @staticmethod
    def get(request, id):
        booking = Booking.objects.get(id=id)
        status_booking = Booking.STATUS_BOOKING
        type_payment = Booking.TYPE_PAYMENT
        type_rooms = TypeRoom.objects.all()
        guests = Guest.objects.all()
        return render(request, 'booking/status.html', locals())

    @staticmethod
    def post(request):
        pass


def user_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return render(request, 'accounts/login.html')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['system_joined'] = datetime.datetime.now().strftime('%d %B %Y %H:%M')
            return redirect('/')
        else:
            return redirect('/login')


def user_logout(request):
    logout(request)
    return redirect('/login')


def user_register(request):
    if request.method == 'GET':
        print(request.user)
        if str(request.user) == 'adminka':
            return render(request, 'accounts/register.html')
        else:
            return redirect('/login')

    if request.method == 'POST':
        pass


class GuestsViews(View):
    @staticmethod
    def get(request):
        guests = Guest.objects.order_by('-id')
        return render(request, 'guests/list-guests.html', locals())

    @staticmethod
    def post(request):
        pass


class TasksViews(View):
    @staticmethod
    def get(request):
        tasks = Task.objects.filter(status=False).order_by('datetime')
        return render(request, 'tasks/list-taks.html', locals())

    @staticmethod
    def post(request):
        pass


class ListBookingViews(View):
    @staticmethod
    def get(request):
        bookings = Booking.objects.filter(stat=True).order_by('-id')
        return render(request, 'booking/list.html', locals())

    @staticmethod
    def post(request):
        pass


def statistics(request):
    r = request.GET.get('date', None)
    if r is None:
        date = datetime.datetime.now().date()
    else:
        print(r)
        # 2019-04-24
        sort = list(map(int, r.split('-')))
        date = datetime.date(sort[2], sort[1], sort[0])

    bookings = Booking.objects.filter(stat=True, date_arrival__date__lte=date, date_departure__date__gte=date)
    hotel_name = settings.HOTEL_NAME

    return render(request, 'statistics.html', locals())


def profile(request):
    sss = request.session['system_joined']
    return render(request, 'accounts/profile.html', locals())


def printer(request, _date):
    sort = list(map(int, _date.split('-')))
    date = datetime.date(sort[2], sort[1], sort[0])

    bookings = Booking.objects.filter(stat=True, date_arrival__date__lte=date, date_departure__date__gte=date)

    return render(request, 'print.html', {'date': date, 'bookings': bookings})


def add_guest(request):
    form_guest = GuestForm()
    return render(request, 'guests/add-guest.html', locals())


def organization(request):
    new_form = OrganizationForm()
    orgs = Organization.objects.all().order_by('-id')
    if request.POST:
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    return render(request, 'organization.html', {'new_form': new_form, 'orgs': orgs})


def print_booking(request, id):
    booking = Booking.objects.get(id=id)
    today = datetime.datetime.now().date()
    hotel_name = settings.HOTEL_NAME
    return render(request, 'booking/print.html', {'booking': booking, 'today': today, 'hotel_name': hotel_name})