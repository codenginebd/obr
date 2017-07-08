$(document).ready(function () {
    $("#id_signin_form").submit(function (e) {
        e.preventDefault();
        var validated = validate_signin_form($("#id_signin_form"));
        if (validated) {
            $("#id_signin_button").prop("disabled", true);
            $("#id_signin_button").text("Signing In...");
            $("#id_signin_button").addClass("signin_disabled");

            var url = $("#id_signin_form").data("action");
            var data = $("#id_signin_form").serialize();
            call_ajax("POST", url, data, function (data) {
                    if (data.status == "SUCCESS") {
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
        }
        else {
            return false
        }
    });

    function validate_signin_form($form_instance) {
        var $username_field = $form_instance.find("#id_username");
        var username = $username_field.val();
        var validated = true;
        if (username == "") {
            validated = false;
            $username_field.next(".signup_field_error").text("This field is required").removeClass("displaynone");
        }
        else {
            if ((is_valid_email_address(username)) || (is_valid_phone_number(username))) {
                $username_field.next(".signup_field_error").text("").addClass("displaynone");
            }
            else {
                validated = false;
                $username_field.next(".signup_field_error").text("Enter a valid Email or Phone").removeClass("displaynone");
            }
        }
        return validated;
    }

    function is_valid_email_address(email_address) {
        var emailRegex = new RegExp(/^([\w\.\-]+)@([\w\-]+)((\.(\w){2,4})+)$/i);
        return emailRegex.test(email_address);
    }

    function is_valid_phone_number(phone_no) {
        var phone_regex = /^[0,1,2,3,4,5,6,7,8,9]{11}$/;
        if (phone_no.match(phone_regex)) {
            return true;
        }
        else {
            return false;
        }
    }
});