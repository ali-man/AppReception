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
                    // цена номера UZS
                    let priceUzs = sel.eq(0).attr('data-room-uzs');
                    // цена номера USD
                    let priceUsd = sel.eq(0).attr('data-room-usd');
                    selectedDisplayPrice(sel.eq(1), priceUzs, priceUsd, sel.length-1);
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
                }
            }
        }
    });

    function selectedDisplayPrice(sel, uzs, usd, len) {
        $(sel).append(
            `<div class="selected-price-info">
                <span class="price">${uzs*len} | ${usd*len} сум</span> 
                <span class="fordays">За <b>${len}</b> суток</span></div>`
        );
    }
    $('#new-booking_add').click(function () {
        let $selected = $('.selected');
        let bookingData = [];
        for (let i = 0; i < $selected.length; i++) {
            if ($selected[i] === $selected[0]) {
                Cookies.set('dateArrival', $($selected[i]).attr('data-day'));
                Cookies.set('nameRoom', $($selected[i]).siblings('.firstcol').children('span.room-name')[0].innerText);
            } else if ($selected.length === 1) {
                Cookies.set('dateDeparture', $($selected[i]).attr('data-day'));
            } else if ($selected[i] === $selected[$selected.length-1]) {
                Cookies.set('dateDeparture', $($selected[i]).attr('data-day'));
            }
        }
        window.location.href = '/booking/';
    });

    $('#new-booking_cancel').click(function () {
        $('#new-booking').hide();
        $('.selected-price-info').remove();
        $('.freeday').removeClass('selected');
    });

    let tdBooking = $('td.booking');
    tdBooking.on({
        mouseover: function () {
            $(this).children('.display-info-booking').show();
        },
        mouseleave: function () {
            $(this).children('.display-info-booking').hide();
        }
    })

});