$(document).ready(function () {
    // let rooms = $('.type-room__room');
    // for (let i = 0; i < rooms.length; i++) {
    //     if ($(rooms[i]).attr('data-booking-id') !== 'freeday') {
    //         let id = $(rooms[i]).attr('data-booking-id');
    //         $.ajax({
    //             url: '/ajax/booking-info/',
    //             method: 'GET',
    //             data: {
    //                 bookingID: id
    //             },
    //             dataType: 'json',
    //             beforeSend: function () {
    //                 console.log('Идёт загрузка данных');
    //             },
    //             success: function (data) {
    //                 $(rooms[i]).addClass(`status${data.fields.status_booking}`);
    //             }
    //         });
    //     }
    // }

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
            // } else if ( dataBookingID.split(' ')[0] === 'status-3' ) {
            //     $(this).append('<i class="fas fa-user-clock"></i>');
        } else {
            let bookingID = dataBookingID.split(' ')[1];
            $(this).css('position', 'relative');
            $('.display_hide').remove();
            $(this).append(
                `<div class="display_hide">
                  <ul data-booking-id="${bookingID}" class="menu-booking-room">
                    <li class="menu-evict" data-toggle="modal" data-target="#evictModal">Выселить</li>
                    <li class="menu-change">Изменить</li>
                    <li class="menu-cancel">Отмена</li>
                  </ul>
                </div>`
            );
            // window.location.href = `/booking/edit-${bookingID}`;
        }

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
                    console.log(data.fields);
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