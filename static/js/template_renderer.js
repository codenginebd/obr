/* Dependencies
*Mustache
*jQuery
*/
(function(window,undefined) {
"use strict"

window.render_template = function(template_name, data, partial, options) {
    try {
        Mustache.compile(template_name);
        return Mustache.render(template_name, data, partial);
    } catch(err) {
        //Mustache is required may be
    }
}

})(window)