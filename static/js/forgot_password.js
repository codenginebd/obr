$(document).ready(function () {
    $("#id_forgot_password_form").submit(function (e) {
        e.preventDefault();
        var validated = validate_forgot_password_form($("#id_forgot_password_form"));
        if (validated) {
            $("#id_forgot_password_button").prop("disabled", true);
            $("#id_forgot_password_button").text("Submitting...");
            $("#id_forgot_password_button").addClass("forgot_password_disabled");

            var url = $("#id_forgot_password_form").data("action");
            var data = $("#id_forgot_password_form").serialize();
            call_ajax("POST", url, data, function (data) {
                    if (data.status == "SUCCESS") {
                        location.href = $("#id_forgot_password_form").data("post-forgot-password-url")+"?email="+data.data.email;
                        $(".forgot_password_error").text("").addClass("displaynone");
                    }
                    else {
                        $(".forgot_password_error").text(data.data.message).removeClass("displaynone");
                    }
                },
                function (jqxhr, status, error) {
                    $(".forgot_password_error").text("Problem with password reset request. Please try again later").removeClass("displaynone");
                },
                function (msg) {
                    $("#id_forgot_password_button").prop("disabled", false);
                    $("#id_forgot_password_button").text("Submit");
                    $("#id_forgot_password_button").removeClass("forgot_password_disabled");
                });
        }
        else {
            return false
        }
    });

    function validate_forgot_password_form($form_instance) {
        var $email = $form_instance.find("#id_email");
        var email = $email.val();
        var validated = true;
        if (email == "") {
            validated = false;
            $email.next(".forgot_password_field_error").text("This field is required").removeClass("displaynone");
        }
        else {
            if ((is_valid_email_address(email))) {
                $email.next(".forgot_password_field_error").text("").addClass("displaynone");
            }
            else {
                validated = false;
                $email.next(".forgot_password_field_error").text("Enter a valid Email").removeClass("displaynone");
            }
        }
        return validated;
    }


    function is_valid_email_address(email_address) {
        var emailRegex = new RegExp(/^([\w\.\-]+)@([\w\-]+)((\.(\w){2,4})+)$/i);
        return emailRegex.test(email_address);
    }
});