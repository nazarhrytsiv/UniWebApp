$(document).ready(function () {
    $(".thing").on('focus', function () {
        $(this).removeClass("invalid");
        $(this).next().addClass("invisible");
    });

    errors_input = new Object();


    $(".thing").on('input', function () {
        if ($(this).hasClass("string")) {
            if (!validate_input_string(this)) {
                errors_input[this["id"]] = false;

            }
            else {
                delete errors_input[this["id"]];
            }
        }
        else if ($(this).hasClass("integer")) {
            if (!validate_input_integer(this)) {
                errors_input[this["id"]] = false;
            }
            else {
                delete errors_input[this["id"]];
            }
        }
    });

    if (jQuery.isEmptyObject(errors_input)) {

        $('#save_thing').on('click', function () {
            var _data = {
                'title': $('#id_title_thing').val(),
                'content': $('#id_content_thing').val(),
                'price': $('#id_price_thing').val(),
            };
            console.log('fffff');
            var count_errors = 0;
            for (let key in _data) {
                if (_data[key].length === 0) {
                    $("#id_" + key + "_thing").addClass("invalid");
                    $("#id_warning_" + key).text("This field is required.").removeClass("invisible");
                    count_errors++;
                }
            }
            if (!count_errors) {
                $.ajax({
                    type: "POST",
                    url: 'http://localhost:8000/create/',
                    contentType: 'application/json; charset=utf-8',
                    data: JSON.stringify(_data),
                    success: function () {
                        window.location.replace('');
                    },
                    error: function (data) {
                        errors = JSON.parse(data.responseText);
                        for (let err in errors) {
                            $("#id_" + err + "_thing").addClass("invalid");
                            $("#id_warning_" + err).text(errors[err]).removeClass("invisible");
                        }
                    }
                });
            }
        });
    }
});
