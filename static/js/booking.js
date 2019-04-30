$(document).ready(function () {

    // console.log(Cookies.get('dateDeparture'));

    $('#rooms').select2();
    if (Cookies.get('room'))
        $('#rooms').val(Cookies.get('room')).trigger("change");

    jQuery('#date-arrival').datetimepicker({
        format: 'd-m-Y',
        value: new Date(),
        timepicker: false
    });
    jQuery('#date-departure').datetimepicker({
        format: 'd-m-Y',
        value: new Date(),
        timepicker: false
    });

    $("#date-arrival-time").datetimepicker({
        datepicker: false,
        format: "H:i",
        value: "13:00"
    });
    $("#date-departure-time").datetimepicker({
        datepicker: false,
        format: "H:i",
        value: "12:00"
    });
    let elementsID = [
        "#source-booking", "#status-booking", "#id_place_of_birth",
        "#id_nationality", "#id_citeznship", "#id_visa", "#price", "#type_payment",
        "#source-booking2", "#status-booking2", "#id_place_of_birth2",
        "#id_nationality2", "#id_citeznship2", "#id_visa2",
        "#source-booking3", "#status-booking3", "#id_place_of_birth3",
        "#id_nationality3", "#id_citeznship3", "#id_visa3"
    ];
    for (let i = 0; i < elementsID.length; i++) fnSelect(elementsID[i]);

    function fnSelect(val) {
        $(val).select2({
            width: '100%',
            tags: true,
            maximumSelected: 1
        });
    }

    $('#price').change(function () {
        if ($('#select2-price-container').attr('title') === 'Своя цена') {
            $('.hide-own-price').show();
        } else {
            $('.hide-own-price').hide();
        }
    });

    $('#source-booking').change(function () {
        if ($('#select2-source-booking-container').attr('title') === 'Hotel System Management') {
            $('.hide-own-source-booking').hide();
        } else {
            $('.hide-own-source-booking').show();
        }
    });

    $('#id_check_date').click(function () {

        let typeRoom = $('#type_rooms').val();
        let dateArrival = $('#date-arrival').val();
        let dateArrivalTime = $('#date-arrival-time').val();
        let dateDepartureTime = $('#date-departure-time').val();
        let dateDeparture = $('#date-departure').val();
        let csrf = $("input[name=csrfmiddlewaretoken]").val();
        console.log(typeRoom, dateArrival, dateArrivalTime, dateDeparture, dateDepartureTime);
        $.ajax({
            url: '/ajax/search-rooms/',
            method: 'GET',
            data: {
                csrfmiddlewaretoken: csrf,
                dateArrival: dateArrival,
                dateArrivalTime: dateArrivalTime,
                dateDeparture: dateDeparture,
                dateDepartureTime: dateDepartureTime,
                typeRoom: typeRoom
            },
            dataType: 'json',
            success: function (data) {
                console.log(data);
            }
        });
    });
    Cookies.remove('room');

    $('.payment-click').click(function () {
        let citeznshipDefault = '7';
        let typeRoom = $('#rooms').val().split('-')[0];
        let dateArrival = fnMoment($('#date-arrival').val());
        let dateDeparture = fnMoment($('#date-departure').val());
        let earlyArrival = false;
        let lateDeparture = false;
        if ($('#id_early_arrival').is(':checked')) earlyArrival = true;
        if ($('#id_late_departure').is(':checked')) lateDeparture = true;
        let citeznship = $('#id_citeznship').val();
        let citeznship2 = $('#id_citeznship2').val();
        let citeznship3 = $('#id_citeznship3').val();
        console.log($('#id_citeznship').val());
        if (citeznship2 === "") citeznship2 = citeznshipDefault;
        if (citeznship3 === "") citeznship3 = citeznshipDefault;

        $.ajax({
            url: '/ajax/info-type-rooms/',
            method: 'GET',
            data: {
                dateArrival: dateArrival,
                dateDeparture: dateDeparture,
                typeRoom: typeRoom
            },
            dataType: 'json',
            success: function (data) {
                console.log(data);
                let price = null;
                // TODO: Сменить на РУЗ гражданство
                if (citeznship === citeznshipDefault && citeznship2 === citeznshipDefault && citeznship3 === citeznshipDefault) {
                    price = data['uzs']
                } else {
                    price = data['usd']
                }
                let days = data.days;

                $('#sutok').text(days);
                $('#prozh').text(price);
                $('#koplate').text(price * days);
                if (earlyArrival) {
                    $('#koplate').text(Number($('#koplate').text()) + (price / 2));
                    $('#sutok').text(Number($('#sutok').text()) + 0.5);
                }
                if (lateDeparture) {
                    $('#koplate').text(Number($('#koplate').text()) + (price / 2));
                    $('#sutok').text(Number($('#sutok').text()) + 0.5);
                }
                $('#id_koplate_i').val(Number($('#prozh').text()));
            }
        });

        $('#answer').click(function () {
            let kOplateI = $('#id_koplate_i').val();
            $('#prozh').text(kOplateI);
            let days = Number($('#sutok').text());
            $('#koplate').text(Number($('#prozh').text()) * days);
        });
    });

    function fnMoment(el) {
        //    19-04-2019
        let elem = el.split('-');
        let year = Number(elem[2]);
        let month = Number(elem[1]);
        let day = Number(elem[0]);
        return [year, month, day]
    }

    $('#btn-guest-2').click(function () {
        $('.guest-2').toggle();
        $('#btn-guest-3').toggle();
    });
    $('#btn-guest-3').click(function () {
        $('.guest-3').toggle();
    });

    $('#save_and_back').click(function () {
        let objDataAll = fnDataAll();
        console.log(objDataAll['dateArrival'])
        $.ajax({
            url: '/ajax/booking-post/',
            method: 'POST',
            data: objDataAll,
            dataType: 'json',
            beforeSend: function () {
                console.log('Идёт сохранение данных');
            },
            success: function (data) {
                window.location.href = '/booking/';
            }
        });
    });

    $('#send-booking').click(function () {
        let objDataAll = fnDataAll();
        $.ajax({
            url: '/ajax/booking-post/',
            method: 'POST',
            data: objDataAll,
            dataType: 'json',
            beforeSend: function () {
                console.log('Идёт сохранение данных');
            },
            success: function (data) {
                window.location.href = '/';
            }
        });
    });

    function fnDataAll() {
        let csrf = $("input[name=csrfmiddlewaretoken]").val();
        let sourceBooking = $('#source-booking').val();
        let numberSourceBooking = $('#number-source-booking').val();
        let room = $('#rooms').val();
        let dateArrival = toList($('#date-arrival').val(), $('#date-arrival-time').val());
        let dateDeparture = toList($('#date-departure').val(), $('#date-departure-time').val());
        let earlyArrival = false;
        let lateDeparture = false;
        if ($('#id_early_arrival').is(':checked')) earlyArrival = true;
        if ($('#id_late_departure').is(':checked')) lateDeparture = true;
        let adminComment = $('#admin-comment').val();
        let customerWishes = $('#customer-wishes').val();

        let organization = $('#id_organization').val();

        let fullname = $('#id_fullname').val();
        let dateOfBirth = $('#id_date_of_birth').val();
        let placeOfBirth = $('#id_place_of_birth').val();
        let passportSerialNumber = $('#id_serial_number').val();
        let passportGivenDate = $('#id_given_date').val();
        let passportExpireDate = $('#id_expire_date').val();
        let passportGiveOrganization = $('#id_give_organization').val();
        let placeOfLiving = $('#id_place_of_living').val();
        let nationality = $('#id_nationality').val();
        let citeznship = $('#id_citeznship').val();

        let phone = $('#id_phone').val();
        let email = $('#id_email').val();

        let kppNumber = $('#id_kpp_number').val();
        let kppDateArrival = $('#id_kpp_date_arrival').val();

        let visaNumber = $('#id_visa_number').val();
        let visaType = $('#id_visa_type').val();
        let visaGivenDate = $('#id_visa_given_date').val();
        let visaExpireDate = $('#id_visa_expire_date').val();

        let fullname2 = $('#id_fullname2').val();
        let dateOfBirth2 = $('#id_date_of_birth2').val();
        let placeOfBirth2 = $('#id_place_of_birth2').val();
        let passportSerialNumber2 = $('#id_serial_number2').val();
        let passportGivenDate2 = $('#id_given_date2').val();
        let passportExpireDate2 = $('#id_expire_date2').val();
        let passportGiveOrganization2 = $('#id_give_organization2').val();
        let placeOfLiving2 = $('#id_place_of_living2').val();
        let nationality2 = $('#id_nationality2').val();
        let citeznship2 = $('#id_citeznship2').val();

        let phone2 = $('#id_phone2').val();
        let email2 = $('#id_email2').val();

        let kppNumber2 = $('#id_kpp_number2').val();
        let kppDateArrival2 = $('#id_kpp_date_arrival2').val();

        let visaNumber2 = $('#id_visa_number2').val();
        let visaType2 = $('#id_visa_type2').val();
        let visaGivenDate2 = $('#id_visa_given_date2').val();
        let visaExpireDate2 = $('#id_visa_expire_date2').val();

        let fullname3 = $('#id_fullname3').val();
        let dateOfBirth3 = $('#id_date_of_birth3').val();
        let placeOfBirth3 = $('#id_place_of_birth3').val();
        let passportSerialNumber3 = $('#id_serial_number3').val();
        let passportGivenDate3 = $('#id_given_date3').val();
        let passportExpireDate3 = $('#id_expire_date3').val();
        let passportGiveOrganization3 = $('#id_give_organization3').val();
        let placeOfLiving3 = $('#id_place_of_living3').val();
        let nationality3 = $('#id_nationality3').val();
        let citeznship3 = $('#id_citeznship3').val();

        let phone3 = $('#id_phone3').val();
        let email3 = $('#id_email3').val();

        let kppNumber3 = $('#id_kpp_number3').val();
        let kppDateArrival3 = $('#id_kpp_date_arrival3').val();

        let visaNumber3 = $('#id_visa_number3').val();
        let visaType3 = $('#id_visa_type3').val();
        let visaGivenDate3 = $('#id_visa_given_date3').val();
        let visaExpireDate3 = $('#id_visa_expire_date3').val();

        let typePayment = $('#type_payment').val();
        let statusBooking = $('#status-booking').val();
        let prozh = $('#prozh').text();

        return {
            csrfmiddlewaretoken: csrf,
            sourceBooking: sourceBooking,
            numberSourceBooking: numberSourceBooking,
            room: room,
            dateArrival: dateArrival,
            earlyArrival: earlyArrival,
            dateDeparture: dateDeparture,
            lateDeparture: lateDeparture,
            adminComment: adminComment,
            customerWishes: customerWishes,
            organization: organization,

            fullname: fullname,
            dateOfBirth: dateOfBirth,
            placeOfBirth: placeOfBirth,
            passportSerialNumber: passportSerialNumber,
            passportGivenDate: passportGivenDate,
            passportExpireDate: passportExpireDate,
            passportGiveOrganization: passportGiveOrganization,
            placeOfLiving: placeOfLiving,
            nationality: nationality,
            citeznship: citeznship,
            phone: phone,
            email: email,
            kppNumber: kppNumber,
            kppDateArrival: kppDateArrival,
            visaNumber: visaNumber,
            visaType: visaType,
            visaGivenDate: visaGivenDate,
            visaExpireDate: visaExpireDate,

            fullname2: fullname2,
            dateOfBirth2: dateOfBirth2,
            placeOfBirth2: placeOfBirth2,
            passportSerialNumber2: passportSerialNumber2,
            passportGivenDate2: passportGivenDate2,
            passportExpireDate2: passportExpireDate2,
            passportGiveOrganization2: passportGiveOrganization2,
            placeOfLiving2: placeOfLiving2,
            nationality2: nationality2,
            citeznship2: citeznship2,
            phone2: phone2,
            email2: email2,
            kppNumber2: kppNumber2,
            kppDateArrival2: kppDateArrival2,
            visaNumber2: visaNumber2,
            visaType2: visaType2,
            visaGivenDate2: visaGivenDate2,
            visaExpireDate2: visaExpireDate2,

            fullname3: fullname3,
            dateOfBirth3: dateOfBirth3,
            placeOfBirth3: placeOfBirth3,
            passportSerialNumber3: passportSerialNumber3,
            passportGivenDate3: passportGivenDate3,
            passportExpireDate3: passportExpireDate3,
            passportGiveOrganization3: passportGiveOrganization3,
            placeOfLiving3: placeOfLiving3,
            nationality3: nationality3,
            citeznship3: citeznship3,
            phone3: phone3,
            email3: email3,
            kppNumber3: kppNumber3,
            kppDateArrival3: kppDateArrival3,
            visaNumber3: visaNumber3,
            visaType3: visaType3,
            visaGivenDate3: visaGivenDate3,
            visaExpireDate3: visaExpireDate3,

            // typePayment: typePayment,
            statusBooking: statusBooking,
            // days: days,
            prozh: prozh,
            // kOptale: kOptale,
            // oplacheno: oplacheno,
            // ostalos: ostalos,
        }
    }

    function toList(date, time) {
        let year, month, day, hours, minute;
        year = Number(date.split('-')[2]);
        month = Number(date.split('-')[1]);
        day = Number(date.split('-')[0]);
        hours = Number(time.split(':')[0]);
        minute = Number(time.split(':')[1]);
        return `${year}, ${month}, ${day}, ${hours}, ${minute}`
    }

    $('#id_search_text').keyup(function () {
        let searchText = $('#id_search_text').val();
        if (searchText.length > 2) {
            $.ajax({
                url: '/ajax/search-guest/',
                method: 'GET',
                data: {
                    searchText: searchText
                },
                dataType: 'json',
                success: function (data) {
                    if (data.error) {
                        $('#result_search_guests').empty();
                        $('#result_search_guests').append(
                            `<span>${data.error}</span>`
                        );
                    } else {
                        $('#result_search_guests').empty();
                        for (let i = 0; i < data.guests.length; i++) {
                            console.log(data.guests);
                            $('#result_search_guests').append(
                                `<span class="result-guest"
                                style="width: 280px; border-radius: 4px; display: inline-block; cursor: pointer; padding: 10px; background-color: #3c61ae; color: #fff; margin-top: 5px;" 
                                data-guest-fullname="${data.guests[i][0]}"
                                data-guest-citezn="${data.guests[i][1]}"
                                >${data.guests[i][0]}</span><br>`
                            );
                        }
                        $('span.result-guest').click(function () {
                            $('#id_fullname').val($(this).attr('data-guest-fullname'));
                            // TODO: гражданство Ajax
                            console.log($(this).attr('data-guest-citezn'));
                            let citezn = $(this).attr('data-guest-citezn');
                            $('#id_citeznship').val(citezn).trigger('change');
                        })
                    }
                }
            });
        }
    });

});