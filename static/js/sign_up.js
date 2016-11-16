$(document).ready(function () {
    $(".signup_field").focusin(function (e) {
        $(this).addClass("bg_white_field")
    }).focusout(function (e) {
        $(this).removeClass("bg_white_field")
    });
    
    function validate_signup_form($form_instance) {
        var $first_name_field = $form_instance.find("#id_first_name");
        var first_name = $first_name_field.val();
        var validated = true;
        if(first_name == "") {
            validated = false;
            $first_name_field.next(".signup_field_error").text("First name is required").removeClass("displaynone");
        }
        else {
            $first_name_field.next(".signup_field_error").text("").addClass("displaynone");
        }
        
        var $last_name_field = $form_instance.find("#id_last_name");
        var last_name = $last_name_field.val();
        var validated = true;
        if(last_name == "") {
            validated = false;
            $last_name_field.next(".signup_field_error").text("last name is required").removeClass("displaynone");
        }
        else {
            $last_name_field.next(".signup_field_error").text("").addClass("displaynone");
        }
        
        var $email_field = $form_instance.find("#id_email");
        var email = $email_field.val();
        var validated = true;
        if(email == "") {
            validated = false;
            $email_field.next(".signup_field_error").text("last name is required").removeClass("displaynone");
        }
        else {
            $email_field.next(".signup_field_error").text("").addClass("displaynone");
        }
        
        var $phone_field = $form_instance.find("#id_phone");
        var phone = $phone_field.val();
        var validated = true;
        if(phone == "") {
            validated = false;
            $phone_field.next(".signup_field_error").text("last name is required").removeClass("displaynone");
        }
        else {
            $phone_field.next(".signup_field_error").text("").addClass("displaynone");
        }
        return validated;
    }
    
    $("#id_signup_form").submit(function (e) {
        e.preventDefault();
        var validated = validate_signup_form($("#id_signup_form"));
        alert(validated);
        return false;
    });
    
});
