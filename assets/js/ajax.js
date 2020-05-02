$(document).ready(function () {
    $(".ajaxSubmit").submit(function (e) {
        const ajaxblock = $(this).attr("data-ajaxblock");
        e.preventDefault();
        $.ajax({
            url: $(this).attr("action"),
            type: "GET",
            data: $(this).serialize(),

            success: function (data) {
                console.log(data)
                $("#"+ ajaxblock).html(data);
            }
        });

    });
})

// Avoid writing action in html
/**
const submitFn = function(url) {
    return function (e) {
        e.preventDefault();
        $.ajax({
            url: url,
            type: "GET",
            data: $(this).serialize(),

            success: function (json) {
                console.log(json)
            }
        });
    }
}

$(document).ready(function () {
    $(".ajaxSubmit").submit(submitFn("http://google.com"));
    $(".ajaxSubmi2").submit(submitFn("http://facebook.com"));
    $(".ajaxSubmi3").submit(submitFn("http://twitter.com"));
})
*/
