$(document).ready(function () {

    $('.mdb-select').materialSelect();

    $('#js-rooms-select').select2({
        width: '100%',
    });

    $('#datetime-picker-in').datetimepicker();

    $('#datetime-picker-out').datetimepicker();

    let cs = $('#table-cell').cellSelection({
        selectClass: '.selected',
        ignoreCell: '.ignore',
    });

    function btnCancelSelected() {
        let btnCancel = $('#cancel_selected_btn');
        btnCancel.show();
        btnCancel.click(function () {
            cs.cellSelection('deselect');
            $(this).hide();
            $('#booking_room_btn').hide();
            $('#booking_rooms_btn').hide();
        });
    }

    function btnBookingRoom() {
        let btnBooking = $('#booking_room_btn');
        btnBooking.show();
    }

    function btnBookingRooms() {
        let btnBooking = $('#booking_rooms_btn');
        btnBooking.show();
    }

    function searchSelected() {
        let selected = $('.selected');
        let roomName = [], dateList = []; // Хранит информацию о номерах и дате

        for (let i = 0; i < selected.length; i++) {

            // TODO: сменить логику получения имени номера, для удаления лишнего атрибута 'data' в тегах html
            let roomNameIter = $(selected[i]).attr('data-room-name'); // Получаем имя номера ячейки. В каждой итерации меняется ячейка
            if (roomName.length === 0) {
                roomName.push(roomNameIter);
            } else {
                if ($.inArray(roomNameIter, roomName) === -1) {
                    roomName.push(roomNameIter);
                }
            }

            let dateListIter = $(selected[i]).attr('data-date'); // Получаем дату ячейки. В каждой итерации меняется ячейка
            if ($.inArray(dateListIter, dateList) === -1) {
                dateList.push(dateListIter);
            }
        }

        return {roomName: roomName, dateList: dateList};
    }

    function bookingRoom() {
    }

    function bookingRooms() {
    }

    // Запуск кода после отпускание ПКМ по ячейке таблицы
    $('td.new_chess-d_k').on('mouseup', function () {
        let selected = searchSelected();

        // Проверка брони на количество номеров, если выбран один номер,
        // запускается модальное окно для брони одного номера,
        // если выбрано больше одного номера, запускается группавая бронь
        if (selected.roomName.length === 1) {
            $('#booking_rooms_btn').hide();
            btnCancelSelected(); // показываем кнопку отмены
            btnBookingRoom();
            console.log('booking room');
        } else if (selected.roomName.length > 1) {
            $('#booking_room_btn').hide();
            btnCancelSelected(); // показываем кнопку отмены
            btnBookingRooms();
            console.log('booking rooms');
        } else {
            alert('Вы не верно указали дни');
        }
    });

    // BOOKING ROOM FORM
    $('#addGuest1').click(function () {
        if ($('#addGuest1').is(':checked')) {
            $('.guest1').slideDown(900);
        } else {
            $('.guest1').slideUp(900);
            $('.guest2').slideUp(900);
            $('#addGuest2').prop('checked', false);
            $('.guest3').slideUp(900);
            $('#addGuest3').prop('checked', false);
        }
    });

    $('#addGuest2').click(function () {
        if ($('#addGuest2').is(':checked')) {
            $('.guest2').slideDown(900);
        } else {
            $('.guest2').slideUp(900);
            $('.guest3').slideUp(900);
            $('#addGuest3').prop('checked', false);
        }
    });

    $('#addGuest3').click(function () {
        if ($('#addGuest3').is(':checked')) {
            $('.guest3').slideDown(900);
        } else {
            $('.guest3').slideUp(900);
        }
    });

});