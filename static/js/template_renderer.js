/* Dependencies
*Mustache
*jQuery
*/
(function(window,undefined) {
"use strict"

window.render_template = function(template_html, data) {
    try {
        var template = Handlebars.compile(template_html);
        return template(data);
    } catch(err) {
        //Mustache is required may be
    }
}

})(window)