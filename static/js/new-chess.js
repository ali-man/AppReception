$(document).ready(function () {

    let cs = $('#table-cell').cellSelection({
        selectClass: 'selected',
        ignoreCell: 'booking' // ячейки с классом '.ignore' не будут выделяться
    });

    // let bookings = $('td.new_chess-d_k');
    // for (let i = 0; i < bookings.length; i++) {
    //     if ($(bookings[i]).attr('data-booking-id') !== 'freeday') $(bookings[i]).css({
    //         // 'background-color': 'green',
    //         'color': 'white',
    //     });
    // }

    let freeRooms = $('ul.free_rooms li');
    $('.free_rooms_quantity').text(freeRooms.length);
    for (let i = 0; i < freeRooms.length; i++) {
        let freeRoomName = $(freeRooms[i]).text();
        let roomsName = $('td.new_chess-r_k');
        for (let j = 0; j < roomsName.length; j++) {
            if ($(roomsName[j]).text() === freeRoomName) {
                $(roomsName[j]).css({
                    // 'background-color': '#b5e8ff',
                    'color': 'green',
                    'font-weight': '600'
                });
            }
        }
    }
    $('ul.free_rooms').css({'display': 'none'});

    $('#date_arrival').datetimepicker({
        format: 'd-m-Y',
        timepicker: false
    });
    $('#date_departure').datetimepicker({
        format: 'd-m-Y',
        timepicker: false
    });

    $('#create_booking_group').click(function () {
        $('#early_arrival_input').val('13:00');
        $('#late_departure_input').val('12:00');

        let roomsName = $('.new_chess-r_k');
        let selecteds = $('.selected');
        let objSelecteds = {};

        for (let i = 0; i < roomsName.length; i++) {
            let roomName = $(roomsName[i]).text();
            objSelecteds[roomName] = []
        }

        for (let i = 0; i < selecteds.length; i++) {
            let roomName = $(selecteds[i]).siblings('td.new_chess-r_k')[0].innerText; //.split('-')[0]
            objSelecteds[roomName].push($(selecteds[i]).attr('data-date'));
        }

        // TODO: Надо чтобы цена бралась из базы
        let priceRooms = {
            'Single Rooms': {'ruz': 200000, 'in': 250000},
            'Twin Rooms': {'ruz': 360000, 'in': 510000},
            'Double Rooms': {'ruz': 360000, 'in': 510000},
            'Lux Rooms': {'ruz': 900000, 'in': 1200000},
            'Apartments': {'ruz': 500000, 'in': 900000},
        };

        $('table.table-group-booking tbody').empty();
        for (let key in objSelecteds) {
            if (objSelecteds[key].length !== 0) {
                let roomName = key.split('-')[0];
                $('table.table-group-booking tbody').append(
                    `<tr>
                    <td>${key}</td>
                    <td>${objSelecteds[key][0]}</td>
                    <td>${objSelecteds[key][objSelecteds[key].length - 1]}</td>
                    <td>${objSelecteds[key].length - 1}</td>
                    <td class="price_room">${priceRooms[roomName].ruz * (objSelecteds[key].length - 1)}/${priceRooms[roomName].in * (objSelecteds[key].length - 1)}</td>
                    </tr>`
                );
            }
        }
        let priceRoom = $('td.price_room');
        let pricesRUZ = 0;
        let pricesIn = 0;
        for (let i = 0; i < priceRoom.length; i++) {
            let ruz = Number(($(priceRoom[i]).text().split('/')[0])); //.replace('  ', '')
            let ino = Number(($(priceRoom[i]).text().split('/')[1])); //.replace('  ', '')
            pricesRUZ += ruz;
            pricesIn += ino;
        }
        $('table.table-group-booking tbody').append(
            `
            <tr>
            <td colspan="3"></td>
            <td><b>Итог: </b></td>
            <td>${to_summ(pricesRUZ)}/${to_summ(pricesIn)}</td>
            </tr>
            `
        );
        $('#send_booking_group').click(function () {
            let org = $('#id_organization_val').val();
            let earlyArrival = $('#early_arrival_input').val();
            let lateDeparture = $('#late_departure_input').val();
            let earlyArrivalCh = false;
            let lateDepartureCh = false;
            if ($('#early_arrival_checkbox').is(':checked')) earlyArrivalCh = true;
            if ($('#late_departure_checkbox').is(':checked')) lateDepartureCh = true;
            $.ajax({
                url: '/ajax/send-booking-group/',
                method: 'get',
                data: {
                    organization: org,
                    earlyArrival: earlyArrival,
                    lateDeparture: lateDeparture,
                    earlyArrivalCh: earlyArrivalCh,
                    lateDepartureCh: lateDepartureCh,
                    roomsBooking: objSelecteds
                },
                dataType: 'json',
                success: function (data) {
                    if (data.ok) window.location.href = '/';
                }
            });
        });
    });

    let calendar = $('.new_chess-d_k');
    let objBookingIDs = {};
    for (let i = 0; i < calendar.length; i++) {
        if ($(calendar[i]).attr('data-booking-id') !== 'freeday') {
            objBookingIDs[$(calendar[i]).attr('data-booking-id')] = $(calendar[i]).attr('data-booking-id');
        }
    }

    function startAjax() {
        $.ajax({
            url: '/ajax/search-booking-id/',
            method: 'get',
            data: objBookingIDs,
            dataType: 'json',
            beforeSend: function () {

            },
            success: function (data) {
                let objs = data;
                for (let i = 0; i < calendar.length; i++) {
                    if ($(calendar[i]).attr('data-booking-id') !== 'freeday') {
                        let timeLet = $(calendar[i]).attr('data-booking-id');
                        let indexOrganization = 0,
                            indexGuests = 1,
                            indexArrival = 2,
                            indexDeparture = 3,
                            indexDays = 4,
                            indexStatusBooking = 5;
                        let guests = objs[timeLet][indexGuests];
                        $(calendar[i]).css({'position': 'relative'});
                        // $(calendar[i]).empty();
                        $(calendar[i]).append(
                            `
                            <div class="b-abs-id">
                            <ul>
                                <li>Организация</li>
                                <li>${objs[timeLet][indexOrganization]}</li>
                                <li>Гости</li>
                                <li>${guests.join(', ')}</li>
                                <li>Дата заезда</li>
                                <li>${objs[timeLet][indexArrival]}</li>
                                <li>Дата выезда</li>
                                <li>${objs[timeLet][indexDeparture]}</li>
                                <li>Ночей</li>
                                <li>${objs[timeLet][indexDays]}</li>
                                <li>Статус брони</li>
                                <li>${objs[timeLet][indexStatusBooking]}</li>
                            </ul>                              
                            </div>
                            `
                        );
                    }
                }
            }
        });
    }

    startAjax();

    $('.new_chess-d_k').on({
        mouseenter: function (event) {
            $(this).css({'cursor': 'pointer'});
            $(this).children('div.b-abs-id').css({'left': event.clientX - 150, 'top': event.clientY + 50});
            $(this).children('div.b-abs-id').show();
        },
        mouseleave: function (event) {
            $(this).children('div.b-abs-id').hide()
        },
        click: function () {
            if ($(this).attr('data-booking-id') !== 'freeday') {
                window.open(`/booking/edit-${$(this).attr('data-booking-id')}`, '_blank');
            }
        }
    });












    $('#rooms').select2();
    $('#id_search_guest_1').select2();
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

    $('#booking_btn_fixed').click(function () {
        let arr = cs.cellSelection('getArray', 'data');
        let fromYear = arr[0].year;
        let fromMonth = arr[0].month;
        let fromDay = arr[0].day;
        let toYear = arr[arr.length - 1].year;
        let toMonth = arr[arr.length - 1].month;
        let toDay = arr[arr.length - 1].day;

        let room = arr[0].room;
        let arrival = `${fromDay}-${fromMonth}-${fromYear}`;
        let departure = `${toDay}-${toMonth}-${toYear}`;

        $('#rooms').val(room).trigger('change');

        $('#date-arrival').datetimepicker({
            format: 'd-m-Y',
            value: arrival,
            // onShow: function (ct) {
            //     this.setOptions({
            //         maxDate: jQuery('#date-departure').val() ? jQuery('#date-departure').val() : false
            //     })
            // },
            timepicker: false
        });
        $('#date-departure').datetimepicker({
            format: 'd-m-Y',
            value: departure,
            // onShow: function (ct) {
            //     this.setOptions({
            //         minDate: jQuery('#date-arrival').val() ? jQuery('#date-arrival').val() : false
            //     })
            // },
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
        fnBooking();
    });

    function fnBooking() {

        $('#send_obj_to_server').click(function () {
            let objDataAll = fnDataAll();
            console.log(objDataAll['earlyArrival']);
            // $.ajax({
            //     url: '/ajax/booking-post/',
            //     method: 'POST',
            //     data: objDataAll,
            //     dataType: 'json',
            //     beforeSend: function () {
            //         console.log('Идёт сохранение данных');
            //     },
            //     success: function (data) {
            //         window.location.href = '/';
            //     }
            // });
        });
    }

    function fnDataAll() {
        // let csrf = $("input[name=csrfmiddlewaretoken]").val();

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
        let days = $('#sutok').text();
        let prozh = $('#prozh').text();
        let kOptale = $('#koplate').text();
        let oplacheno = $('#oplacheno').text();
        let ostalos = $('#ostalos').text();

        return {
            // csrfmiddlewaretoken: csrf,
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

            typePayment: typePayment,
            statusBooking: statusBooking,
            days: days,
            prozh: prozh,
            kOptale: kOptale,
            oplacheno: oplacheno,
            ostalos: ostalos,
        };

        function toList(date, time) {
            let year, month, day, hours, minute;
            year = Number(date.split('-')[2]);
            month = Number(date.split('-')[1]);
            day = Number(date.split('-')[0]);
            hours = Number(time.split(':')[0]);
            minute = Number(time.split(':')[1]);
            return `${year}, ${month}, ${day}, ${hours}, ${minute}`
        }
    }

    function fnSelects(room, arrival, departure) {

    }

    function fnMoment(el) {
        //    19-04-2019
        let elem = el.split('-');
        let year = Number(elem[2]);
        let month = Number(elem[1]);
        let day = Number(elem[0]);
        return [year, month, day]
    }

    $('#payment-tab').click(function () {
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
        if (citeznship2 === "") citeznship2 = 'UZBEKISTAN';
        if (citeznship3 === "") citeznship3 = 'UZBEKISTAN';
        // let oplachenoI = $('#id_oplacheno_i').val(0);
        // let oplacheno = $('#oplacheno').text(0);

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
                if (citeznship, citeznship2, citeznship3 === 'UZBEKISTAN') {
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
                $('#id_koplate_i').val(Number($('#koplate').text()));
            }
        });

        $('#answer').click(function () {
            // oplachenoI = $('#id_oplacheno_i').val();
            let kOplateI = $('#id_koplate_i').val();
            $('#koplate').text(kOplateI);
            let days = Number($('#sutok').text());
            $('#prozh').text(kOplateI / days);
            // $('#oplacheno').text(oplachenoI);
            // $('#ostalos').text(kOplateI - oplachenoI);
        });
    });

});