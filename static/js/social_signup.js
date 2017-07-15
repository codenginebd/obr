/**
 * Created by zia ahmed on 7/14/2017.
 */

$(document).ready(function () {

    function check_phone_number_used(value, url, success_callback, error_callback, complete_callback) {
        call_ajax("GET", url, {"value": value},
            success_callback, error_callback, complete_callback);
    }

    function check_email_used(value, url, success_callback, error_callback, complete_callback) {
        call_ajax("GET", url, {"value": value},
            success_callback, error_callback, complete_callback);
    }

    function is_valid_phone_number($field) {
        var phoneno = /^[1,2,3,4,5,6,7,8,9]{10}$/;
        if (($field.val().match(phoneno))) {
            return true;
        }
        else {
            return false;
        }
    }

    function id_valid_email_address(email_address) {
        var emailRegex = new RegExp(/^([\w\.\-]+)@([\w\-]+)((\.(\w){2,4})+)$/i);
        var valid = emailRegex.test(email_address);
        return valid
    }

    function register_only_for_numeric_input(element_id, max_length_allowed) {
        if (typeof max_length_allowed == 'undefined') {
            max_length_allowed = 10;
        }
        $("#" + element_id).keypress(function (e) {
            //e.preventDefault();
            if (e.keyCode >= 48 && e.keyCode <= 57) {
                if ($(this).val().length >= max_length_allowed) {
                    return false;
                }
                return true;
            }
            else {
                return false;
            }
        });
    }

    register_only_for_numeric_input("id_phone", 10);

    $(".signup_field").focusin(function (e) {
        $(this).addClass("bg_white_field")
    }).focusout(function (e) {
        $(this).removeClass("bg_white_field")
    });

    var $signup_form_instance = $("#id_social_signup_form");


    var email_available = true;
    var phone_available = true;

    var $email_field = $signup_form_instance.find("#id_email.signup_field");
    $email_field.focusin(function (e) {
        $email_field.next(".signup_field_error").text("").addClass("displaynone");
    }).focusout(
        function (e) {
            var email = $email_field.val();
            if (email == "") {
                $email_field.next(".signup_field_error").text("This field is required").removeClass("displaynone");
            }
            else {
                if (!id_valid_email_address(email)) {
                    $email_field.next(".signup_field_error").text("Enter a valid email address").removeClass("displaynone");
                }
                else {
                    check_email_used(email, $signup_form_instance.data("check-email-url"),
                        function (data) {
                            if (data.status == "SUCCESS") {
                                if (data.code == 1) {
                                    email_available = false;
                                    var $email_field = $signup_form_instance.find("#id_email");
                                    $email_field.next(".signup_field_error").text("This email is not available").removeClass("displaynone");
                                }
                                else {
                                    var $email_field = $signup_form_instance.find("#id_email");
                                    $email_field.next(".signup_field_error").text("").addClass("displaynone");
                                }
                            }
                        },
                        function (jqxhr, status, error) {

                        },
                        function (msg) {

                        });
                }
            }
        }
    );

    var $phone_field = $signup_form_instance.find("#id_phone.signup_field");
    $phone_field.focusin(function (e) {
        $phone_field.next(".signup_field_error").text("").addClass("displaynone");
    }).focusout(
        function (e) {
            var phone = $phone_field.val();
            if (phone == "") {
                $phone_field.parent().next(".signup_field_error").text("This field is required").removeClass("displaynone");
            }
            else {
                $phone_field.removeClass('signup_field');
                if (!is_valid_phone_number($phone_field)) {
                    $phone_field.parent().next(".signup_field_error").text("Enter a valid phone number").removeClass("displaynone");
                }
                else {
                    check_phone_number_used(phone, $signup_form_instance.data("check-phone-url"),
                        function (data) {
                            if (data.status == "SUCCESS") {
                                if (data.code == 1) {
                                    phone_available = false;
                                    var $phone_field = $signup_form_instance.find("#id_phone");
                                    $phone_field.parent().next(".signup_field_error").text("This phone number is not available").removeClass("displaynone");
                                }
                                else {
                                    $phone_field.parent().next(".signup_field_error").text("").addClass("displaynone");
                                }
                            }
                        },
                        function (jqxhr, status, error) {

                        },
                        function (msg) {

                        });
                }
            }
        }
    );

    function validate_signup_form($form_instance) {
        var $email_field = $form_instance.find("#id_email");
        var email = $email_field.val();
        var validated = true;
        if (email == "") {
            validated = false;
            $email_field.next(".signup_field_error").text("This field is required").removeClass("displaynone");
        }
        else {
            if (!id_valid_email_address(email)) {
                validated = false;
                $email_field.next(".signup_field_error").text("Enter a valid email address").removeClass("displaynone");
            }
            else {
                $email_field.next(".signup_field_error").text("").addClass("displaynone");
            }
        }

        var $phone_field = $form_instance.find("#id_phone");
        var phone = $phone_field.val();
        var validated = true;
        if (phone == "") {
            validated = false;
            $phone_field.parent().next(".signup_field_error").text("This field is required").removeClass("displaynone");
        }
        else {
            if (!is_valid_phone_number($phone_field)) {
                validated = false;
                $phone_field.parent().next(".signup_field_error").text("Enter a valid phone number").removeClass("displaynone");
            }
            else {
                $phone_field.parent().next(".signup_field_error").text("").addClass("displaynone");
            }
        }
        return validated;
    }

    $("#id_social_signup_form").submit(function (e) {
        e.preventDefault();
        var validated = validate_signup_form($("#id_social_signup_form"));
        if (validated) {
            if (email_available && phone_available) {
                var url = $("#id_social_signup_form").data("action");
                var account_activate_url = $("#id_social_signup_form").data("account-activate-url");
                var data = $("#id_social_signup_form").serialize();
                window.call_ajax("POST", url, data,
                    function (data) {
                        var account_activate_data = {
                            'email': data.data.email
                        };
                        if (data.data.success_url) {
                            location.href = data.data.success_url;
                        } else {
                            window.call_ajax("GET", account_activate_url, account_activate_data,
                                function (result) {
                                    location.href = $("#id_social_signup_form").data("post-signup-url") + "?email=" + result.data.email;
                                },
                                function (jqxhr, status, error) {

                                },
                                function (msg) {

                                });
                        }
                    },
                    function (jqxhr, status, error) {

                    },
                    function (msg) {

                    })
            }
            else {
                return false;
            }
        }
        else {
            return false;
        }
        return false;
    });

});


window.fbAsyncInit = function () {
    var facebook_app_id = $("#id_signup_form").data("facebook_app_id");
    FB.init({
        appId: facebook_app_id,
        status: true, // check login status
        cookie: true, // enable cookies to allow the server to access the session
        xfbml: true  // parse XFBML
    });
};

(function (d) {
    var js, id = 'facebook-jssdk', ref = d.getElementsByTagName('script')[0];
    if (d.getElementById(id)) {
        return;
    }
    js = d.createElement('script');
    js.id = id;
    js.async = true;
    js.src = "https://connect.facebook.net/en_US/all.js";
    ref.parentNode.insertBefore(js, ref);
}(document));

function facebook_signin() {
    FB.login(function (response) {
        if (response.status === 'connected') {
            console.log('connected');
            getInfo(response.authResponse.accessToken);
        }
        else if (response.status === 'not_authorized') {
            console.log('not_authorized');
        }
        else {
            console.log('else');
        }
    }, {scope: 'email'});
}

function getInfo(authkey) {
    FB.api('/me?fields=id,email,first_name,last_name', function (response) {
        location.href = $("#id_signup_form").data("social-signup-url") +
            "?email=" + response.email + "&first_name=" + response.first_name +
            "&last_name=" + response.last_name;
    });
}