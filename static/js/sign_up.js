$(document).ready(function () {
    function password_checker(password_value) {
        var matched_value = password_value.match(/^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])([a-zA-Z0-9]{6,})$/)
        if (matched_value) {
            return true;
        }
        return false;
    }

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
    };

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

    var $signup_form_instance = $("#id_signup_form");


    var email_available = true;
    var phone_available = true;

    $signup_form_instance.find("#id_password").tooltip({
        'trigger': 'focus',
        'class': 'red-tooltip',
        'title': 'Password should be minimum 6 characters long with at least 1 capital letter, 1 digit and 1 number'
    });
    $signup_form_instance.find("#id_password2").tooltip({
        'trigger': 'focus',
        'title': 'Password should be minimum 6 characters long with at least 1 capital letter, 1 digit and 1 number'
    });

    var $first_name_field = $signup_form_instance.find("#id_first_name");
    $first_name_field.focusin(function (e) {
        $first_name_field.next(".signup_field_error").text("").addClass("displaynone");
    }).focusout(
        function (e) {
            var first_name = $first_name_field.val();
            if (first_name == "") {
                $first_name_field.next(".signup_field_error").text("This field is required").removeClass("displaynone");
            }
            else {
                $first_name_field.next(".signup_field_error").text("").addClass("displaynone");
            }
        }
    );

    var $last_name_field = $signup_form_instance.find("#id_last_name");
    $last_name_field.focusin(function (e) {
        $last_name_field.next(".signup_field_error").text("").addClass("displaynone");
    }).focusout(
        function (e) {
            var last_name = $last_name_field.val();
            if (last_name == "") {
                $last_name_field.next(".signup_field_error").text("This field is required").removeClass("displaynone");
            }
            else {
                $last_name_field.next(".signup_field_error").text("").addClass("displaynone");
            }
        }
    );

    var $email_field = $signup_form_instance.find("#id_email");
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

    var $phone_field = $signup_form_instance.find("#id_phone");
    $phone_field.focusin(function (e) {
        $phone_field.next(".signup_field_error").text("").addClass("displaynone");
    }).focusout(
        function (e) {
            var phone = $phone_field.val();
            if (phone == "") {
                $phone_field.parent().next(".signup_field_error").text("This field is required").removeClass("displaynone");
            }
            else {
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


    var $password_field = $signup_form_instance.find("#id_password");
    $password_field.focusin(function (e) {
        $password_field.parent().find(".signup_field_error").text("").addClass("displaynone");
    }).focusout(
        function (e) {
            var password = $password_field.val();
            if (password == "") {
                $password_field.parent().find(".signup_field_error").text("This field is required").removeClass("displaynone");
            }
            else {
                if (!password_checker(password)) {
                    $password_field.parent().find(".signup_field_error").text("Enter a strong password").removeClass("displaynone");
                }
                else {
                    $password_field.parent().find(".signup_field_error").text("").addClass("displaynone");
                }
            }
        }
    );

    var $password2_field = $signup_form_instance.find("#id_password2");
    $password2_field.focusin(function (e) {
        $password2_field.parent().find(".signup_field_error").text("").addClass("displaynone");
    }).focusout(
        function (e) {
            var password = $signup_form_instance.find("#id_password").val();
            var password2 = $password2_field.val();
            if (password2 == "") {
                $password2_field.parent().find(".signup_field_error").text("This field is required").removeClass("displaynone");
            }
            else {
                if (password != password2) {
                    $password2_field.parent().find(".signup_field_error").text("Password mismatch").removeClass("displaynone");
                }
                else {
                    if (!password_checker(password2)) {
                        $password2_field.parent().find(".signup_field_error").text("Enter a strong password").removeClass("displaynone");
                    }
                    else {
                        $password2_field.parent().find(".signup_field_error").text("").addClass("displaynone");
                    }
                }
            }
        }
    );


    function validate_signup_form($form_instance) {
        var $first_name_field = $form_instance.find("#id_first_name");
        var first_name = $first_name_field.val();
        var validated = true;
        if (first_name == "") {
            validated = false;
            $first_name_field.next(".signup_field_error").text("This field is required").removeClass("displaynone");
        }
        else {
            $first_name_field.next(".signup_field_error").text("").addClass("displaynone");
        }

        var $last_name_field = $form_instance.find("#id_last_name");
        var last_name = $last_name_field.val();
        var validated = true;
        if (last_name == "") {
            validated = false;
            $last_name_field.next(".signup_field_error").text("This field is required").removeClass("displaynone");
        }
        else {
            $last_name_field.next(".signup_field_error").text("").addClass("displaynone");
        }

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

        var $password_field = $form_instance.find("#id_password");
        var password = $password_field.val();
        var validated = true;
        if (password == "") {
            validated = false;
            $password_field.next(".signup_field_error").text("This field is required").removeClass("displaynone");
        }
        else {
            if (!password_checker(password)) {
                validated = false;
                $password_field.parent().find(".signup_field_error").text("Enter a strong password").removeClass("displaynone");
            }
            else {
                $password_field.parent().find(".signup_field_error").text("").addClass("displaynone");
            }
        }

        var $password2_field = $form_instance.find("#id_password2");
        var password2 = $password2_field.val();
        var validated = true;
        if (password2 == "") {
            validated = false;
            $password2_field.next(".signup_field_error").text("This field is required").removeClass("displaynone");
        }
        else {
            if (password != password2) {
                validated = false;
                $password2_field.next(".signup_field_error").text("Password mismatch").removeClass("displaynone");
            }
            else {
                if (!password_checker(password2)) {
                    validated = false;
                    $password2_field.parent().find(".signup_field_error").text("Enter a strong password").removeClass("displaynone");
                }
                else {
                    $password2_field.parent().find(".signup_field_error").text("").addClass("displaynone");
                }
            }
        }


        return validated;
    }

    $("#id_signup_form").submit(function (e) {
        e.preventDefault();
        var validated = validate_signup_form($("#id_signup_form"));
        if (validated) {
            if (email_available && phone_available) {
                var url = $("#id_signup_form").data("action");
                var account_activate_url = $("#id_signup_form").data("account-activate-url");
                var data = $("#id_signup_form").serialize();
                window.call_ajax("POST", url, data,
                    function (data) {
                        var account_activate_data = {
                            'email': data.data.email
                        };
                        window.call_ajax("GET", account_activate_url, account_activate_data,
                            function (result) {
                                location.href = $("#id_signup_form").data("post-signup-url") + "?email=" + result.data.email;
                            },
                            function (jqxhr, status, error) {

                            },
                            function (msg) {

                            });
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
