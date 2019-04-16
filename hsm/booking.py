import arrow

from hsm.models import Guest, City, Nationality, Citeznship, Visa, Booking, Rooms, TypeRoom, TypePayment, SourceBooking


def timestamp(_date): #, _time
    date = _date
    # time = _time
    day = int(date.split('-')[0])
    month = int(date.split('-')[1])
    year = int(date.split('-')[2])
    # time = int(time.split(':')[0])
    time_stamp = arrow.get(year, month, day).timestamp
    return time_stamp


def request_processing(req):
    guest = {
        'fullname': req['fullname'],
        'date_of_birth': req['date_of_birth'],
        'place_of_birth': req['place_of_birth'],
        'serial_number': req['serial_number'],
        'given_date': req['given_date'],
        'expire_date': req['expire_date'],
        'give_organization': req['give_organization'],
        'place_of_living': req['place_of_living'],
        'nationality': req['nationality'],
        'citeznship': req['citeznship']
    }
    visa = {
        'number': req['visa_number'],
        'type': req['visa_type'],
        'given_date': req['visa_given_date'],
        'expire_date': req['visa_expire_date']
    }
    booking = {
        'source-booking': req['source-booking'],
        'number-source-booking': req['number-source-booking'],
        'rooms': req['rooms'],
        'price': req['price'],
        'own-price-num': req['own-price-num'],
        'date-arrival': timestamp(req['date-arrival']), #, req['date-arrival-time']
        'date-arrival-time': req['date-arrival-time'],
        'date-departure': timestamp(req['date-departure']), #, req['date-departure-time']
        'date-departure-time': req['date-departure-time'],
        'status-booking': int(req['status-booking']),
        'admin-comment': req['admin-comment'],
        'customer-wishes': req['customer-wishes']
    }
    result = {
        'guest': guest,
        'visa': visa,
        'booking': booking}
    return result


def visa_register(_visa):
    try:
        visa = Visa.objects.get(number=_visa['number'])
        # print(visa)
    except Visa.DoesNotExist:
        visa = Visa(
            number=_visa['number'],
            visa_type=_visa['type'],
            given_date=_visa['given_date'],
            expire_date=_visa['expire_date'],
        )
        visa.save()
    print(visa)
    return visa


def guest_register(visa, req):
    try:
        place_of_birth = City.objects.get(name=req['place_of_birth'])
    except City.DoesNotExist:
        place_of_birth = City(name=req['place_of_birth'])
        place_of_birth.save()

    try:
        nationality = Nationality.objects.get(name=req['nationality'])
    except Nationality.DoesNotExist:
        nationality = Nationality(name=req['nationality'])
        nationality.save()
    try:
        citeznship = Citeznship.objects.get(name=req['citeznship'])
    except Citeznship.DoesNotExist:
        citeznship = Citeznship(name=req['citeznship'])
        citeznship.save()

    try:
        guest = Guest.objects.get(serial_number=req['serial_number'])
    except Guest.DoesNotExist:
        guest = Guest()
        print('guest')
        guest.full_name = req['fullname']
        # guest.save()
        # print('fullname')
        guest.date_of_birth = req['date_of_birth']
        # guest.save()
        # print('date_of_birth')
        guest.place_of_birth = place_of_birth
        # guest.save()
        # print('place_of_birth_id')
        guest.serial_number = req['serial_number']
        # guest.save()
        # print('serial_number')
        guest.given_date = req['given_date']
        # guest.save()
        # print('given_date')
        guest.expire_date = req['expire_date']
        # guest.save()
        # print('expire_date')
        guest.give_organization = req['give_organization']
        # guest.save()
        # print('give_organization')
        guest.place_of_living = req['place_of_living']
        # guest.save()
        # print('place_of_living')
        guest.nationality = nationality
        # guest.save()
        # print('nationality_id')
        guest.citeznship = citeznship
        # guest.save()
        # print('citeznship_id')
        guest.visa = visa
        guest.save()
        print('visa_id')

    return guest


def booking_register(guest, kwargs):
    # print(guest)
    # print(kwargs['type_payment'])
    print(kwargs['rooms'])
    r = kwargs['rooms'].split('-')
    type_room = TypeRoom.objects.get(name=r[0])
    room = Rooms.objects.get(type_room=type_room, number_room=r[-1])

    a = arrow.get(kwargs['date-arrival'])
    b = arrow.get(kwargs['date-departure'])
    days = (b.datetime - a.datetime).days
    if kwargs['price'] == 'fixed-price':
        price = type_room.price
    else:
        price = int(kwargs['own-price-num'])
    price_all = price * days
    # try:
    #     type_payment = TypePayment.objects.get(name=kwargs['type_payment'])
    # except TypeRoom.DoesNotExist:
    #     type_payment = TypeRoom(name=kwargs['type_payment'])
    #     type_payment.save()
    try:
        source_of_booking = SourceBooking.objects.get(name=kwargs['source-booking'])
    except SourceBooking.DoesNotExist:
        source_of_booking = SourceBooking(name=kwargs['source-booking'])
        source_of_booking.save()

    booking = Booking(
        room=room,
        date_of_arrival=kwargs['date-arrival'],
        date_of_arrival_time=kwargs['date-arrival-time'],
        date_of_departure=kwargs['date-departure'],
        date_of_departure_time=kwargs['date-departure-time'],
        price_per_night=price,
        price_for_all_time=price_all,
        # type_payment=type_payment,
        source_of_booking=source_of_booking,
        number_source_booking=kwargs['number-source-booking'] if kwargs['number-source-booking'] else '',
        status_booking=kwargs['status-booking'],
        admin_comment=kwargs['admin-comment'],
        customer_wishes=kwargs['customer-wishes'],
        # task=kwargs['task'],
    )
    booking.save()
    booking.guest.add(guest)
    booking.save()
