$(document).ready(function () {
    $(".product").on('focus', function () {
        $(this).removeClass("invalid");
        $(this).next().addClass("invisible");
    });
    $('#save_product').on('click', function () {
        var _data = {
                'title': $('#id_title_product').val(),
                'description': $('#id_description_product').val(),
                'price': $('#id_price_product').val(),
                'image': null,
                'sale':  $('#id_sale_product').is(':checked')
            };
        $.ajax({
            type: "POST",
            url: 'http://localhost:8000/products/create/',
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



function update_product(slug) {
    $(".product").on('focus', function () {
        $(this).removeClass("invalid");
        $(this).next().addClass("invisible");
    });
    var _data = {
        'slug': slug,
        'title': $('#id_title_product').val(),
        'description': $('#id_description_product').val(),
        'price': $('#id_price_product').val(),
        'image': null,
        'sale':  $('#id_sale_product').is(':checked')
    };

    $.ajax({
        type: "PUT",
        url: '/products/' + slug + '/edit/',
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify(_data),
        success: function (response) {
            console.log('edited');
        },
        error: function (data) {
            errors = JSON.parse(data.responseText);
            for (let err in errors) {
                $("#id_" + err + "_room").addClass("invalid");
                $("#id_warning_" + err).text(errors[err]).removeClass("invisible");
            }
        }
    });
}