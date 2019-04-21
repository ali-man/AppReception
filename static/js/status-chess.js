$(document).ready(function () {

    let currentStatSB = $('#current_stat_status_booking').text();
    let currentStatTP = $('#current_stat_type_payment').text();
    let currentStatRoom = $('#current_stat_rooms').text();
    $('#id_status_booking').select2({width: 250});
    $('#id_status_booking').val(currentStatSB).trigger("change");
    $('#id_type_payment').select2();
    $('#id_type_payment').val(currentStatTP).trigger("change");
    // $('#id_rooms').val(currentStatRoom).trigger('change');
    console.log(currentStatRoom);
    $('#id_rooms').select2({
        width: 250
    });
    $('#id_rooms').val(currentStatRoom).trigger("change");

    $('#guests').select2({
        width: 590,
        tags: true,
        // tokenSeperators: [',', ' ']
    });

    let guestSelected = $('.guest_selected');
    for (let i = 0; i < guestSelected.length; i++) {
        let idGuest = $(guestSelected[i]).attr('data-guest-id');
        $('#guests').val(idGuest).trigger('change');
    }

    $('#status_save').click(function () {
        let bookingID = $('#id_booking_id').text();
        let guestsID = $('#guests').val();
        let statusBooking = $('#id_status_booking').val();
        let paid = $('#id_paid').val();
        let typePayment = $('#id_type_payment').val();
        let rooms = $('#id_rooms').val();
        let adminComments = $('#id_admin_comment').val();
        let customerWishes = $('#id_customer_wishes').val();
        $.ajax({
            url: '/ajax/status-booking-change/',
            method: 'GET',
            data: {
                bookingID: bookingID,
                guestsID: guestsID,
                statusBooking: statusBooking,
                paid: paid,
                typePayment: typePayment,
                rooms: rooms,
                adminComments: adminComments,
                customerWishes: customerWishes
            },
            dataType: 'json',
            success: function (data) {
                // console.log(guestsID);
                window.location.href = '/';
            }
        });
    });

    $('#status_remove').click(function () {
        let bookingID = $('#id_booking_id').text();
        $.ajax({
            url: '/ajax/status-booking-remove/',
            method: 'GET',
            data: {bookingID:bookingID},
            dataType: 'json',
            success: function (data) {
                window.location.href = '/';
            }
        })
    })

});