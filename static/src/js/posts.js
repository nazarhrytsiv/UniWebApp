$(document).ready(function () {
    $(".item").on('focus', function () {
        $(this).removeClass("invalid");
        $(this).next().addClass("invisible");
    });
    $('#save_thing').on('click', function () {
        var _data = {
                'title': $('#id_title_thing').val(),
                'content': $('#id_content_thing').val(),
                'price': $('#id_price_thing').val(),
            };
        $.ajax({
            type: "POST",
            url: 'http://localhost:8000/thingcr/',
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify(_data),
            success: function (_data) {
                console.log('created!');
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

