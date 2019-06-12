$(document).ready(function () {

    let today = new Date();
    let year = today.getFullYear();
    let month = today.getMonth();
    let date = today.getDate();

    $.ajax({
        url: '/ajax/today-date/',
        method: 'get',
        data: {},
        dataType: 'json',
        success: function (data) {
            if (data.ok) {
                console.log(data.ok);
            } else {
                console.log(data.error);
            }
        }
    });

    function fnBooking() {

        $('#send_obj_to_server').click(function () {
            let objDataAll = fnDataAll();
            console.log(objDataAll['earlyArrival']);
        });
    }

    $('#filter_date').datetimepicker({
        format: 'd-m-Y',
        timepicker: false
    });

    $('.type-room__room').click(function () {
        let dataBookingID = $(this).attr('data-booking-id');
        let room = this.textContent;
        let typeRoom = $($(this).parent().children('.type_room'))[0].innerText;
        Cookies.set('room', `${typeRoom}-${this.textContent}`);
        if (dataBookingID === 'freeday') {
            window.location.href = '/booking/';
        } else {
            let bookingID = dataBookingID.split(' ')[1];
            if (bookingID === 'dirty') {
                $(this).css('position', 'relative');
                $('.display_hide').remove();
                $(this).append(
                    `<div class="display_hide">
                      <ul data-booking-id="${room}" class="menu-booking-room">
                        <li class="menu-cleaning">Чистый</li>
                        <li class="menu-cancel">Отмена</li>
                      </ul>
                    </div>`
                );
            } else {
                $(this).css('position', 'relative');
                $('.display_hide').remove();
                $(this).append(
                    `<div class="display_hide">
                      <ul data-booking-id="${bookingID}" class="menu-booking-room">
                        <li class="menu-evict" data-toggle="modal" data-target="#evictModal">Выселить</li>
                        <li class="menu-change">Изменить</li>
                        <li class="menu-services">Услуги</li>
                        <li class="menu-cancel">Отмена</li>
                      </ul>
                    </div>`
                );
            }

            // window.location.href = `/booking/edit-${bookingID}`;
        }

        $('li.menu-services').click(function () {
            let bookingID = $(this).parent().attr('data-booking-id');
            Cookies.set('bookingID', Number(bookingID));
            $.ajax({
                url: '/ajax/services-info/',
                method: 'get',
                data: {
                    bookingID: bookingID
                },
                dataType: 'json',
                success: function (data) {
                    console.log(data);
                    if (data.debt) {
                        window.location.href = `/services/edit-${data.id}`;
                    }
                    if (data.error) {
                        window.location.href = '/services/create';
                    }
                }
            });
        });

        $('li.menu-cleaning').click(function () {
            let roomNumber = $(this).parent().attr('data-booking-id');
            $.ajax({
                url: '/ajax/cleaning/',
                method: 'get',
                data: {
                    roomNumber: roomNumber
                },
                dataType: 'json',
                success: function (data) {
                    window.location.href = '/';
                }
            });
        });

        $('li.menu-evict').click(function () {
            let bookingID = $(this).parent().attr('data-booking-id');
            // $('#exampleModalLabel').text('Single Room - 4');
            $('.booking_id').text(bookingID);
            $.ajax({
                url: '/ajax/booking-info/',
                method: 'get',
                data: {
                    bookingID: bookingID
                },
                dataType: 'json',
                success: function (data) {
                    // console.log(data);
                    if (data.fields) {
                        // let room = data.fields.room;
                        let statusBooking = data.fields.status_booking;
                        let days = data.fields.days;
                        let leftToPay = data.fields.left_to_pay;
                        let paid = data.fields.paid;
                        let pricePerNight = data.fields.price_per_night;
                        let priceAllTime = data.fields.price_for_all_time;

                        // $('#exampleModalLabel').text(`Номер: ${room}`);
                        let bStatus = $('.booking_status');
                        switch (statusBooking) {
                            case -1:
                                bStatus.text('Бронь без оплаты');
                                break;
                            case 1:
                                bStatus.text('Бронь с предоплатой');
                                break;
                            case -2:
                                bStatus.text('Размещение гостя с долгом');
                                break;
                            case 2:
                                bStatus.text('Размещение гостя с оплатой');
                                break;
                        }
                        $('.booking_price_night').text(pricePerNight);
                        $('.booking_price_days').text(days);
                        $('.booking_price_all').text(priceAllTime);
                        $('.booking_price_paid').text(paid);
                        $('.booking_price_left_pay').text(leftToPay);
                    }
                }
            });

            $.ajax({
                url: '/ajax/services-info/',
                method: 'get',
                data: {
                    bookingID: bookingID
                },
                dataType: 'json',
                success: function (data) {
                    // console.log(data);
                    if (data.debt !== "0") {
                        $('.debt').html(
                            `
                            <a href="/services/edit-${data.id}">Долг за услуги ${data.debt}</a>
                            `
                        );
                    }
                }
            });

            $('#evict_send').click(function () {
                let csrf = $("input[name=csrfmiddlewaretoken]").val();
                let bookingID = $('.booking_id').text();
                let nal = $('#id_nal').val();
                let terminal = $('#id_terminal').val();
                let transfer = $('#id_transfer').val();
                let usd = $('#id_usd').val();

                $.ajax({
                    url: '/ajax/evict-send/',
                    method: 'post',
                    data: {
                        csrfmiddlewaretoken: csrf,
                        bookingID: bookingID,
                        nal: nal,
                        terminal: terminal,
                        transfer: transfer,
                        usd: usd
                    },
                    dataType: 'json',
                    success: function (data) {
                        if (data.ok) {
                            window.open(`/booking/print-${bookingID}`, '_blank');
                            window.location.href = '/';
                        }
                    }
                });
            });
        });

        $('li.menu-change').click(function () {
            let bookingID = $(this).parent().attr('data-booking-id');
            window.location.href = `/booking/edit-${bookingID}`;
        });

        $('li.menu-cancel').click(function () {
            window.location.href = '/';
        })

    });

});