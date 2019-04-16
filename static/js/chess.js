$(document).ready(function () {

    let dataObj = {};
    let $freeday = $('.freeday');
    $freeday.on({
        mousedown: function (e) {
            if (e.button === 0) {
                if (!$(this).hasClass('selected')) {
                    $(this).toggleClass('selected');
                    $freeday.on('mouseenter', function () {
                        $(this).toggleClass('selected');
                    })
                }
            }
        },
        mouseup: function (e) {
            if (e.button === 0) {
                if ($(this).hasClass('selected')) {
                    $freeday.off('mouseenter');
                    $('#new-booking').show();
                    let sel = $('.selected');
                    // Начальная дата брони
                    let start = sel.eq(0).attr('title').split(', ')[0];
                    // Конечная дата брони
                    let end = sel.eq(sel.length - 1).attr('title').split(', ')[0];
                    // Хранение даты начало и конца
                    dataObj.date = [];
                    dataObj.date.push(start);
                    dataObj.date.push(end);
                    // newBooking(dataObj);
                    console.log(dataObj.date);
                    $('#date_timepicker_start').val(start);
                    $('#date_timepicker_end').val(end);
                    // let formatDate = 'DD-MM-YYYY';
                    // let start = moment().format(formatDate);
                    // let end = moment().format(formatDate);
                    // console.log(start);
                    // console.log(end);
                }
            }
        }
    });

    $('#new-booking_cancel').click(function () {
        $('#new-booking').hide();
        $('.freeday').removeClass('selected');
    })

});