import datetime
import json

from django.core import serializers
from django.shortcuts import render, redirect

from django.http import JsonResponse, HttpResponse

from hsm.models import TypeRoom, Booking, Organization, Guest, Nationality, Citeznship, Visa, SourceBooking, Rooms, \
    City, Checks


def to_datetime(_date, _time):
    date = list(map(int, _date.split('-')))
    time = list(map(int, _time.split(':')))
    return datetime.datetime(date[2], date[1], date[0], time[0], time[1])


def str_to_int(dates):
    dt = list(map(int, dates.split(', ')))
    return datetime.datetime(dt[0], dt[1], dt[2], dt[3], dt[4])


def ajax_today_date(request):
    today = datetime.datetime.now().date()
    bookings = Booking.objects.exclude(status_booking=-3).filter(stat=True)

    guests_birthday = []
    for b in bookings:
        for g in b.guest.all():
            if '-' in g.date_of_birth:
                gd_list = list(map(int, g.date_of_birth.split('-')))
            if '.' in g.date_of_birth:
                gd_list = list(map(int, g.date_of_birth.split('.')))

            guest_date_of_birth = datetime.date(gd_list[2], gd_list[1], gd_list[0])

            if today.month == guest_date_of_birth.month and today.day == guest_date_of_birth.day:
                guests_birthday.append(g.full_name)

    if len(guests_birthday) != 0:
        return JsonResponse({'ok': guests_birthday})
    else:
        return JsonResponse({'error': 'Not guests'})


def ajax_booking_info(request):
    booking_id = int(request.GET['bookingID'])
    booking = Booking.objects.get(pk=booking_id)
    data = serializers.serialize('json', [booking])
    struct = json.loads(data)
    data = json.dumps(struct[0])
    return HttpResponse(data, content_type="application/json")


def ajax_services_info(request):
    print(request.GET)
    booking_id = int(request.GET['bookingID'])
    booking = Booking.objects.get(pk=booking_id)
    try:
        service = booking.services.get_debt()
        service_id = booking.services.id
        return JsonResponse({'debt': service, 'id': service_id})
    except Booking.services.RelatedObjectDoesNotExist:
        return JsonResponse({'error': 'Нет услуг'})


def ajax_search_rooms(request):
    # TODO: Вывод свободных номеров
    req = request.GET
    type_room = req['typeRoom']
    date_arrival = to_datetime(req['dateArrival'], req['dateArrivalTime'])
    date_departure = to_datetime(req['dateDeparture'], req['dateDepartureTime'])
    data = {'ok': 'good!'}
    return JsonResponse(data)


def ajax_info_type_rooms(request):
    r = request.GET
    print(r)
    da = list(map(int, r.getlist('dateArrival[]')))
    dd = list(map(int, r.getlist('dateDeparture[]')))
    date_arrival = datetime.date(da[0], da[1], da[2])
    date_departure = datetime.date(dd[0], dd[1], dd[2])
    print(date_arrival)
    days = (date_departure - date_arrival).days
    type_rooms = TypeRoom.objects.get(name=r['typeRoom'])

    data = {
        'uzs': type_rooms.price_uzs,
        'usd': type_rooms.price_usd,
        'days': days
    }
    print(data)
    return JsonResponse(data)


def ajax_booking_post(request):
    if request.method == 'POST':
        r = request.POST
        try:
            guest = Guest.objects.get(full_name=r['fullname'])
        except Guest.DoesNotExist:
            try:
                nationality_id = int(r['nationality'])
                nationality = Nationality.objects.get(id=nationality_id)
            except ValueError:
                try:
                    nationality = Nationality.objects.get(name=r['nationality'])
                except Nationality.DoesNotExist:
                    nationality = Nationality(name=r['nationality'])
                    nationality.save()

            try:
                citeznship_id = int(r['citeznship'])
                citeznship = Citeznship.objects.get(id=citeznship_id)
            except ValueError:
                try:
                    citeznship = Citeznship.objects.get(name=r['citeznship'])
                except Citeznship.DoesNotExist:
                    citeznship = Citeznship(name=r['citeznship'])
                    citeznship.save()

            guest = Guest()
            guest.full_name = r['fullname']
            guest.date_of_birth = r['dateOfBirth']
            guest.serial_number = r['passportSerialNumber']
            guest.given_date = r['passportGivenDate']
            guest.expire_date = r['passportExpireDate']
            guest.give_organization = r['passportGiveOrganization']
            guest.place_of_living = r['placeOfLiving']
            guest.nationality = nationality
            guest.citeznship = citeznship

            guest.phone = r['phone']
            guest.email = r['email']

            guest.kpp_number = r['kppNumber']
            guest.kpp_date_arrival = r['kppDateArrival']

            if r['visaNumber'] != '':
                try:
                    visa = Visa.objects.get(number=r['visaNumber'])
                except Visa.DoesNotExist:
                    visa = Visa()
                    visa.number = r['visaNumber']
                    visa.visa_type = r['visaType']
                    visa.given_date = r['visaGivenDate']
                    visa.expire_date = r['visaExpireDate']
                    visa.save()

                guest.visa = visa

            guest.save()

        if r['fullname2'] != '':
            try:
                guest2 = Guest.objects.get(full_name=r['fullname2'])
            except Guest.DoesNotExist:
                try:
                    nationality2_id = int(r['nationality2'])
                    nationality2 = Nationality.objects.get(id=nationality2_id)
                except ValueError:
                    try:
                        nationality2 = Nationality.objects.get(name=r['nationality2'])
                    except Nationality.DoesNotExist:
                        nationality2 = Nationality(name=r['nationality2'])
                        nationality2.save()

                try:
                    citeznship2_id = int(r['citeznship2'])
                    citeznship2 = Citeznship.objects.get(id=citeznship2_id)
                except ValueError:
                    try:
                        citeznship2 = Citeznship.objects.get(name=r['citeznship2'])
                    except Citeznship.DoesNotExist:
                        citeznship2 = Citeznship(name=r['citeznship2'])
                        citeznship2.save()

                guest2 = Guest()
                guest2.full_name = r['fullname2']
                guest2.date_of_birth = r['dateOfBirth2']
                guest2.serial_number = r['passportSerialNumber2']
                guest2.given_date = r['passportGivenDate2']
                guest2.expire_date = r['passportExpireDate2']
                guest2.give_organization = r['passportGiveOrganization2']
                guest2.place_of_living = r['placeOfLiving2']
                guest2.nationality = nationality2
                guest2.citeznship = citeznship2

                guest2.phone = r['phone2']
                guest2.email = r['email2']

                guest2.kpp_number = r['kppNumber2']
                guest2.kpp_date_arrival = r['kppDateArrival2']

                if r['visaNumber2'] != '':
                    try:
                        visa2 = Visa.objects.get(number=r['visaNumber2'])
                    except Visa.DoesNotExist:
                        visa2 = Visa(number=['visaNumber2'])
                        visa2.visa_type = r['visaType2']
                        visa2.given_date = r['visaGivenDate2']
                        visa2.expire_date = r['visaExpireDate2']
                        visa2.save()

                    guest2.visa = visa2

                guest2.save()

        if r['fullname3'] != '':
            try:
                guest3 = Guest.objects.get(full_name=r['fullname3'])
            except Guest.DoesNotExist:
                try:
                    nationality3_id = int(r['nationality3'])
                    nationality3 = Nationality.objects.get(id=nationality3_id)
                except ValueError:
                    try:
                        nationality3 = Nationality.objects.get(name=r['nationality3'])
                    except Nationality.DoesNotExist:
                        nationality3 = Nationality(name=r['nationality3'])
                        nationality3.save()

                try:
                    citeznship3_id = int(r['citeznship3'])
                    citeznship3 = Citeznship.objects.get(id=citeznship3_id)
                except ValueError:
                    try:
                        citeznship3 = Citeznship.objects.get(name=r['citeznship3'])
                    except Citeznship.DoesNotExist:
                        citeznship3 = Citeznship(name=r['citeznship3'])
                        citeznship3.save()

                guest3 = Guest()
                guest3.full_name = r['fullname3']
                guest3.date_of_birth = r['dateOfBirth3']
                guest3.serial_number = r['passportSerialNumber3']
                guest3.given_date = r['passportGivenDate3']
                guest3.expire_date = r['passportExpireDate3']
                guest3.give_organization = r['passportGiveOrganization3']
                guest3.place_of_living = r['placeOfLiving3']
                guest3.nationality = nationality3
                guest3.citeznship = citeznship3

                guest3.phone = r['phone3']
                guest3.email = r['email3']

                guest3.kpp_number = r['kppNumber3']
                guest3.kpp_date_arrival = r['kppDateArrival3']

                if r['visaNumber3'] != '':
                    try:
                        visa3 = Visa.objects.get(number=r['visaNumber3'])
                    except Visa.DoesNotExist:
                        visa3 = Visa(number=['visaNumber3'])
                        visa3.visa_type = r['visaType3']
                        visa3.given_date = r['visaGivenDate3']
                        visa3.expire_date = r['visaExpireDate3']
                        visa3.save()

                    guest3.visa = visa3

                guest3.save()

        user = request.user
        sourceBooking = SourceBooking.objects.get(name=r['sourceBooking'])
        numberSourceBooking = r['numberSourceBooking']
        rr = r['room'].split('-')
        type_room = TypeRoom.objects.get(name=rr[0])
        room = Rooms.objects.get(type_room=type_room, number_room=rr[-1])
        dateArrival = str_to_int(r['dateArrival'])
        dateDeparture = str_to_int(r['dateDeparture'])
        adminComment = r['adminComment']
        customerWishes = r['customerWishes']

        if r['organization'] != '':
            try:
                organization_id = int(r['organization'])
                organization = Organization.objects.get(id=organization_id)
            except ValueError:
                try:
                    organization = Organization.objects.get(name=r['organization'])
                except Organization.DoesNotExist:
                    organization = Organization(name=r['organization'])
                    organization.save()

        statusBooking = int(r['statusBooking'])
        prozh = r['prozh']
        early_arrival = True if r['earlyArrival'] == 'true' else False
        late_departure = True if r['dateDeparture'] == 'true' else False

        booking = Booking()
        booking.user = user
        booking.source_of_booking = sourceBooking
        if numberSourceBooking != '':
            booking.number_source_booking = numberSourceBooking
        booking.room = room
        booking.date_arrival = dateArrival
        booking.date_departure = dateDeparture
        booking.early_arrival = early_arrival
        booking.late_departure = late_departure
        if adminComment != '':
            booking.admin_comment = adminComment
        if customerWishes != '':
            booking.customer_wishes = customerWishes
        if r['organization'] != '':
            booking.organization = organization
        # booking.type_payment = typePayment
        booking.status_booking = statusBooking
        # booking.days = days
        booking.price_per_night = prozh
        # booking.price_for_all_time = kOptale
        # booking.paid = oplacheno
        # booking.left_to_pay = ostalos
        booking.save()
        booking.guest.add(guest)
        booking.save()
        if r['fullname2'] != '':
            booking.guest.add(guest2)
            booking.save()
        if r['fullname3'] != '':
            booking.guest.add(guest3)
            booking.save()

        return JsonResponse({'ok': 'lets go!'})


def ajax_guest_add(request):
    r = request.POST
    try:
        guest = Guest.objects.get(full_name=r['fullname'])
    except Guest.DoesNotExist:
        try:
            nationality_id = int(r['nationality'])
            nationality = Nationality.objects.get(id=nationality_id)
        except ValueError:
            try:
                nationality = Nationality.objects.get(name=r['nationality'])
            except Nationality.DoesNotExist:
                nationality = Nationality(name=r['nationality'])
                nationality.save()

        try:
            citeznship_id = int(r['citeznship'])
            citeznship = Citeznship.objects.get(id=citeznship_id)
        except ValueError:
            try:
                citeznship = Citeznship.objects.get(name=r['citeznship'])
            except Citeznship.DoesNotExist:
                citeznship = Citeznship(name=r['citeznship'])
                citeznship.save()
        guest = Guest()
        guest.full_name = r['fullname']
        guest.date_of_birth = r['dateOfBirth']
        guest.serial_number = r['passportSerialNumber']
        guest.given_date = r['passportGivenDate']
        guest.expire_date = r['passportExpireDate']
        guest.give_organization = r['passportGiveOrganization']
        guest.place_of_living = r['placeOfLiving']
        guest.nationality = nationality
        guest.citeznship = citeznship

        guest.phone = r['phone']
        guest.email = r['email']

        guest.kpp_number = r['kppNumber']
        guest.kpp_date_arrival = r['kppDateArrival']

        if r['visaNumber'] != '':
            try:
                visa = Visa.objects.get(number=r['visaNumber'])
            except Visa.DoesNotExist:
                visa = Visa()
                visa.number = r['visaNumber']
                visa.visa_type = r['visaType']
                visa.given_date = r['visaGivenDate']
                visa.expire_date = r['visaExpireDate']
                visa.save()

            guest.visa = visa

        guest.save()

    return JsonResponse({'ok': 'Added New Guest'})


def ajax_search_guest(request):
    st = request.GET['searchText']
    guests = Guest.objects.filter(full_name__istartswith=st)
    if str(guests) == '<QuerySet []>':
        return JsonResponse({'error': 'Гость в базе не найден'})
    else:
        data = []
        for i in guests:
            print(i.citeznship)
            data.append([i.full_name, str(i.citeznship)])
        return JsonResponse({'guests': data})


def ajax_status_booking_change(request):
    r = request.GET
    booking_id = int(r['bookingID'])
    guests = list(map(int, r.getlist('guestsID[]')))
    status_booking = int(r['statusBooking'])
    paid = int(r['paid'])
    type_payment = int(r['typePayment'])
    type_room = r['rooms'].split('-')[0]
    type_rooms = TypeRoom.objects.get(name=type_room)
    room = Rooms.objects.get(type_room=type_rooms, number_room=r['rooms'].split('-')[1])
    admin_comment = r['adminComments']
    customer_wishes = r['customerWishes']

    booking = Booking.objects.get(id=booking_id)
    for i in guests:
        guest = Guest.objects.get(id=i)
        booking.guest.add(guest)
    booking.status_booking = status_booking
    booking.left_to_pay -= paid
    booking.paid += paid
    booking.type_payment = type_payment
    booking.room = room
    booking.admin_comment = admin_comment
    booking.customer_wishes = customer_wishes
    booking.stat = True
    booking.save()

    return JsonResponse({'ok': 'jobs!'})


def ajax_status_booking_remove(request):
    booking = Booking.objects.get(id=request.GET['bookingID'])
    booking.stat = False
    booking.save()

    return JsonResponse({'ok': 'remove obj'})


def ajax_new_chess(request):
    bookings = Booking.objects.filter(stat=True)
    type_rooms = TypeRoom.objects.all()
    today = datetime.datetime.now()
    for i in range(-2, 13):
        date = (today + datetime.timedelta(days=i)).date()

    data = serializers.serialize('json', bookings)
    return HttpResponse(data, content_type="application/json")


def ajax_evict_send(request):
    r = request.POST
    booking_id = int(r['bookingID'])
    booking = Booking.objects.get(id=booking_id)
    try:
        nal = int(r['nal'])
        booking.payment_nal += nal
    except ValueError:
        pass
    try:
        terminal = int(r['terminal'])
        booking.payment_terminal += terminal
    except ValueError:
        pass
    try:
        transfer = int(r['transfer'])
        booking.payment_bez_nal += transfer
    except ValueError:
        pass
    try:
        usd = int(r['usd'])
        booking.payment_usd += usd
    except ValueError:
        pass

    booking.status_booking = -3
    booking.save()
    room = Rooms.objects.get(id=booking.room.id)
    room.clean = False
    room.save()

    return JsonResponse({'ok': 'good!'})


def ajax_send_booking_group(request):
    r = request.GET
    dn = 'roomsBooking'
    for tr in TypeRoom.objects.all():
        for room in tr.rooms_set.all():
            if r.getlist(F'{dn}[{room}][]'):
                date_in = to_datetime(r.getlist(F'{dn}[{room}][]')[0], r['earlyArrival'])
                date_out = to_datetime(r.getlist(F'{dn}[{room}][]')[-1], r['lateDeparture'])
                booking_group = Booking()
                booking_group.user = request.user
                booking_group.room = room
                booking_group.date_arrival = date_in
                booking_group.date_departure = date_out
                booking_group.status_booking = -1
                booking_group.price_per_night = 0
                if r['earlyArrivalCh'] == 'true':
                    booking_group.early_arrival = True
                if r['lateDepartureCh'] == 'true':
                    booking_group.late_departure = True
                try:
                    org = Organization.objects.get(name=r['organization'])
                except Organization.DoesNotExist:
                    org = Organization(name=r['organization'])
                    org.save()
                booking_group.organization = org
                booking_group.save()
    return JsonResponse({'ok': 'yeah!'})


def status_booking(num):
    return {
        -1: 'Бронь без оплаты',
        1: 'Бронь с оплатой',
        -2: 'Размещение без оплаты',
        2: 'Размещение с оплатой',
        -3: 'Выселенное размещение',
        3: 'Резерв',
        -4: 'Гости сегодня выезжают',
        4: 'Блокировка номера',
    }[num]


def ajax_search_booking_id(request):
    print(request.GET)
    bookings = Booking.objects.all()
    list_bookings = {}
    for k, v in request.GET.items():
        b = bookings.get(id=int(v))
        list_bookings[b.id] = []
        list_bookings[b.id].append('' if b.organization is None else b.organization.name)
        list_bookings[b.id].append([g.full_name for g in b.guest.all()])
        list_bookings[b.id].append(b.date_arrival.strftime('%d-%m-%Y %H:%M'))
        list_bookings[b.id].append(b.date_departure.strftime('%d-%m-%Y %H:%M'))
        list_bookings[b.id].append(b.days)
        list_bookings[b.id].append(status_booking(b.status_booking))
    return JsonResponse(list_bookings)


def ajax_bookings_change(request):
    if request.user.is_anonymous:
        return redirect('/')
    booking_ids = request.GET.getlist('bookingIDs[]', None)
    status_booking = int(request.GET['statusBooking'])

    if booking_ids is None:
        pass
    booking_ids = list(map(int, booking_ids))
    for i in booking_ids:
        b = Booking.objects.get(id=i)
        b.status_booking = status_booking
        b.save()

    return JsonResponse({'ok': 'yuhu'})


def ajax_bookings_extend(request):
    if request.user.is_anonymous:
        return redirect('/')
    booking_ids = request.GET.getlist('bookingIDs[]', None)
    days = int(request.GET['days'])

    if booking_ids is None:
        pass
    booking_ids = list(map(int, booking_ids))
    for i in booking_ids:
        b = Booking.objects.get(id=i)
        b.date_departure += datetime.timedelta(days=days)
        b.save()

    return JsonResponse({'ok': 'yuhu'})


def ajax_check_print(request):
    if request.user.is_anonymous:
        return redirect('/login')
    r = request.GET
    check_number = int(r['checkNumber'])
    booking_id = int(r['bookingID'])
    booking = Booking.objects.get(id=booking_id)
    check = Checks()
    check.check_number = int(check_number)
    check.booking = booking
    check.kassir = request.user
    check.save()

    return JsonResponse({'ok': 'yeah'})


def ajax_cleaning(request):
    room_number = request.GET['roomNumber']
    room = Rooms.objects.get(number_room=room_number)
    room.clean = True
    room.save()
    return JsonResponse({'ok': 'clean'})
