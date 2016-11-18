window.call_ajax = function (type, url, data, success_callback, error_callback, complete_callback) {
    $.ajax({
            type: type,
            url: url,
            data: data,
            success: function(data)
            {
                var data = jQuery.parseJSON(data);
                if(typeof success_callback == "function") {
                    success_callback(data);
                }
            },
            error: function(jqxhr, status, error)
            {
                if(typeof error_callback == "function") {
                    error_callback(jqxhr, status, error);
                }
            }
        })
        .done(function( msg ) {
            if(typeof complete_callback == "function") {
                    complete_callback(msg);
                }
        });
}