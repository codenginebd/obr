// This is called with the results from from FB.getLoginStatus().
function statusChangeCallback(response) {
    console.log('statusChangeCallback');
    console.log(response);
    // The response object is returned with a status field that lets the
    // app know the current login status of the person.
    // Full docs on the response object can be found in the documentation
    // for FB.getLoginStatus().
    if (response.status === 'connected') {
        // Logged into your app and Facebook.
        getInfo(response.authResponse.accessToken);
    }
    else if (response.status === 'not_authorized') {
        console.log('not_authorized');
    }
    else {
        console.log('else');
    }
}

// This function is called when someone finishes with the Login
// Button.  See the onlogin handler attached to it in the sample
// code below.
function checkLoginState() {
    FB.getLoginStatus(function (response) {
        statusChangeCallback(response);
    });
}

window.fbAsyncInit = function () {
    var facebook_app_id = $("#id_signin_form").data("facebook_app_id");
    FB.init({
        appId: facebook_app_id,
        cookie: true,  // enable cookies to allow the server to access
                       // the session
        xfbml: true,  // parse social plugins on this page
        version: 'v2.8' // use graph api version 2.8
    });

    FB.getLoginStatus(function (response) {
        statusChangeCallback(response);
    });

};

// Load the SDK asynchronously
(function (d, s, id) {
    var js, fjs = d.getElementsByTagName(s)[0];
    if (d.getElementById(id)) return;
    js = d.createElement(s);
    js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));

// Here we run a very simple test of the Graph api after login is
// successful.  See statusChangeCallback() for when this call is made.
function getInfo(authkey) {
    FB.api('/me?fields=id,email,first_name,last_name', function (response) {
        console.log('Good to see you, ' + response.id + '.');
        console.log(response.email);
        var url = $("#id_signin_form").data("social_login_url");
        var _data = {
            'email': response.email
        };
        call_ajax("GET", url, _data, function (data) {
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
        // location.href = $("#id_signup_form").data("social-signup-url") +
        //     "?email=" + response.email + "&first_name=" + response.first_name +
        //     "&last_name=" + response.last_name;
    });
}