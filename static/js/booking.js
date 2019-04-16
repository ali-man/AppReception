$(document).ready(function () {

    $("#rooms").select2();

    jQuery('#date-arrival').datetimepicker({
        format: 'd-m-Y',
        onShow: function (ct) {
            this.setOptions({
                maxDate: jQuery('#date-departure').val() ? jQuery('#date-departure').val() : false
            })
        },
        timepicker: false
    });
    jQuery('#date-departure').datetimepicker({
        format: 'd-m-Y',
        onShow: function (ct) {
            this.setOptions({
                minDate: jQuery('#date-arrival').val() ? jQuery('#date-arrival').val() : false
            })
        },
        timepicker: false
    });

    $("#date-arrival-time").datetimepicker({
        datepicker: false,
        format: "H:i",
        value: "12:00"
    });
    $("#date-departure-time").datetimepicker({
        datepicker: false,
        format: "H:i",
        value: "13:00"
    });

    $("#id_date_of_birth").datetimepicker({
        format: 'd-m-Y',
        timepicker: false
    });

    let elementsID = [
        "#source-booking", "#status-booking", "#id_place_of_birth",
        "#id_nationality", "#id_citeznship", "#id_visa"
    ];
    for (let i = 0; i < elementsID.length; i++) fnSelect(elementsID[i]);

    function fnSelect(val) {
        $(val).select2({
            width: '100%',
            tags: true,
            maximumSelected: 1
        });
    }


    // $('#send-booking').click(function () {
    //     let csrf = $("input[name=csrfmiddlewaretoken]").val();
    //     console.log(csrf);
    //     // $.ajax({
    //     //     url: 'booking/',
    //     //     method: 'post',
    //     //     data: {},
    //     //     dataType: 'json',
    //     //     beforeSend: function () {
    //     //         console.log('Идёт отправка');
    //     //     },
    //     //     success: function () {
    //     //
    //     //     }
    //     // })
    //     // let json = JSON.stringify({csrfmiddlewaretoken: csrf});
    //     let json = {csrfmiddlewaretoken: csrf, qwe: 'qwe'};
    //     let request = new XMLHttpRequest();
    //     request.open('POST', '/booking/');
    //     request.setRequestHeader('Content-type', 'multipart/form-data; charset=utf-8');
    //     request.onreadystatechange = function () {
    //         if (request.readyState === 4 && request.status === 200)
    //             document.getElementById('output').innerHTML=request.responseText;
    //     };
    //     request.send(json);
    // })
});