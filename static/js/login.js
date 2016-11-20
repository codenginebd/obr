$(document).ready(function () {
    $("#id_signin_form").submit(function (e) {
        e.preventDefault();
        $("#id_signin_button").prop("disabled", true);
        $("#id_signin_button").text("Signing In...");
        $("#id_signin_button").addClass("signin_disabled");
        var url = $("#id_signin_form").data("action");
        var data = $("#id_signin_form").serialize();
        call_ajax("POST", url, data, function (data) {
            if(data.status == "SUCCESS") {
                location.href = data.data.url;
                $(".signin_error").text("").addClass("displaynone");
            }
            else {
                $(".signin_error").text(data.data.message).removeClass("displaynone");
            }
        },
        function (jqxhr, status, error) {
            $(".signin_error").text("Problem with sign in. Please try again later").removeClass("displaynone");
        },
        function (msg) {
            $("#id_signin_button").prop("disabled", false);
            $("#id_signin_button").text("Sign In");
            $("#id_signin_button").removeClass("signin_disabled");
        });
        return false;
    });
});