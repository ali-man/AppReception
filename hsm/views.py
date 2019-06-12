import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.base import View

from hsm.booking import guest_register, request_processing, visa_register, booking_register
from hsm.forms import GuestForm, EditBookingForm, StatusForm, OrganizationForm
from hsm.functions import int_to_str
from hsm.models import TypeRoom, SourceBooking, Booking, Guest, Task, Organization, Checks, Services, PaymentServices


class HomeViews(View):
    @staticmethod
    def get(request):
        if request.user.is_anonymous:
            return redirect('/login')
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
        today_resident = bookings.filter(date_arrival__date__lte=date, date_departure__date__gte=date).exclude(
            status_booking=-3).order_by('-id')
        today_booking = len(today_resident)
        today_free = settings.ROOMS_QUANTITY - today_booking
        # Граждан РУЗ
        guests_ruz = len(today_resident.filter(guest__citeznship_id=settings.CITEZNSHIP_RUZ))
        # Граждан Рф
        guests_rf = len(today_resident.filter(guest__citeznship_id=settings.CITEZNSHIP_RF))
        # Граждан Ин
        guests_in = len(today_resident.exclude(guest__citeznship_id=settings.CITEZNSHIP_RUZ).exclude(
            guest__citeznship_id=settings.CITEZNSHIP_RF))
        type_rooms = TypeRoom.objects.all()

        today = datetime.datetime.now().date()
        bookings_for_birth = bookings.exclude(status_booking=-3)

        guests_birthday = []
        for b in bookings_for_birth:
            for g in b.guest.all():
                if '-' in g.date_of_birth:
                    gd_list = list(map(int, g.date_of_birth.split('-')))
                if '.' in g.date_of_birth:
                    gd_list = list(map(int, g.date_of_birth.split('.')))

                guest_date_of_birth = datetime.date(gd_list[2], gd_list[1], gd_list[0])

                if today.month == guest_date_of_birth.month and today.day == guest_date_of_birth.day:
                    guests_birthday.append(g)

        return render(request, 'home.html', locals())

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

    result_sum = {
        'individual': 0,
        'contragent': 0,
        'nal': 0,
        'terminal': 0,
        'bez_nal': 0,
        'usd': 0,
        'itogo': 0,
        'saldo': 0,

        'proj': 0,
        'uehal': 0
    }
    for i in bookings:
        result_sum['nal'] += i.payment_nal
        result_sum['terminal'] += i.payment_terminal
        result_sum['bez_nal'] += i.payment_bez_nal
        result_sum['usd'] += i.payment_usd
        result_sum['saldo'] += i.left_to_pay
        if i.organization:
            result_sum['contragent'] += i.paid
        else:
            result_sum['individual'] += i.paid
        if i.status_booking == -3:
            result_sum['uehal'] += 1
        else:
            result_sum['proj'] += 1

    result_sum['itogo'] = result_sum['individual'] + result_sum['contragent']

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
    check = Checks.objects.all().order_by('-id')[0]
    return render(request, 'booking/print.html', {
        'booking': booking,
        'today': today,
        'hotel_name': hotel_name,
        'check_number': check.check_number + 1
    })


def checks_list(request):
    checks = Checks.objects.all()

    return render(request, 'checks-guest.html', {'checks': checks})


class ListServicesViews(ListView):
    queryset = Services.objects.all().order_by('-id')
    context_object_name = 'services'
    template_name = 'services/list.html'


class EditServicesViews(View):
    @staticmethod
    def get(request, pk):
        service = Services.objects.get(id=pk)
        return render(request, 'services/edit.html', {
            'service': service
        })

    @staticmethod
    def post(request, pk):
        try:
            if request.POST['paid'] == 'paid':
                service = Services.objects.get(id=pk)
                service.paid = service.get_price_all()
                service.save()
                return redirect(F'/services/edit-{pk}')
        except KeyError:
            pass
        nums = range(1, 5)
        name_services = []
        price_services = []
        for n in nums:
            name_services.append(request.POST[F'name{n}'])
            price_services.append(request.POST[F'price{n}'])
        service = Services.objects.get(id=pk)
        for i in range(len(name_services)):
            if price_services[i] != '':
                payment_service = PaymentServices()
                payment_service.service = service
                payment_service.name = name_services[i]
                payment_service.price = int(price_services[i])
                payment_service.save()
        return redirect(F'/services/edit-{pk}')


class CreateServicesViews(View):
    @staticmethod
    def get(request):
        return render(request, 'services/create.html')

    @staticmethod
    def post(request):
        nums = range(1, 11)
        booking_id = request.POST['booking_id'] if request.POST['booking_id'] != '' else None
        print(booking_id)
        name_services = []
        price_services = []
        for n in nums:
            name_services.append(request.POST[F'name{n}'])
            price_services.append(request.POST[F'price{n}'])
        service = Services()
        if booking_id is not None:
            booking = Booking.objects.get(id=int(booking_id))
            service.booking = booking
        service.save()
        for i in range(len(name_services)):
            if price_services[i] != '':
                payment_service = PaymentServices()
                payment_service.service = service
                payment_service.name = name_services[i]
                payment_service.price = int(price_services[i])
                payment_service.save()

        return redirect('/services/list')
