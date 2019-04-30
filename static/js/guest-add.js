$(document).ready(function () {

    let elementsID = [
        "#id_place_of_birth",
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

    $('#send-guest').click(function () {
        let objDataAll = fnDataAll();
        $.ajax({
            url: '/ajax/guest-add/',
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

        return {
            csrfmiddlewaretoken: csrf,
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
            visaExpireDate: visaExpireDate
        }
    }

});