$(document).ready(function () {
    $(".product").on('focus', function () {
        $(this).removeClass("invalid");
        $(this).next().addClass("invisible");
    });
    $('#save_mail').on('click', function () {
        var _data = {
                'title': $('#id_title_mail').val(),
                'text_mail': $('#id_text_mail').val(),
                'mail_from': $('#id_from_mail').val(),
                'mail_to': $('#id_to_mail').val(),
            };
        $.ajax({
            type: "POST",
            url: 'http://localhost:8000/send_mail/',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(_data),
            success: function (_data) {
                console.log('sent!');
            },
            error: function (data) {
                errors = JSON.parse(data.responseText);
                for (let err in errors) {
                    $("#id_" + err + "_user").addClass("invalid");
                    $("#id_warning_" + err).text(errors[err]).removeClass("invisible");
                }
            }
        });
    });
});