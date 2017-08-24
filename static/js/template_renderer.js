/* Dependencies
*Mustache
*jQuery
*/
(function(window,undefined) {
"use strict"

window.render_template = function(template, data, partial, options) {
    try {
        Mustache.parse(template);
        return Mustache.render(template, data, partial);
    } catch(err) {
        //Mustache is required may be
    }
}

})(window)