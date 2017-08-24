$(document).ready(function () {
   $(document).on("click", ".btn-browse-filter", function (e) {
        e.preventDefault();
        $("#id_browse_more_filter_content").slideToggle(500);
    });

    $(document).on("click", ".search-filter-by-category", function (e) {
        if($(this).is(":checked")) {

            call_ajax("GET", "/api/v1/category-browse/", { "pid": $(this).val() },
            function (data) {
                var cat_template = $("#id_search_category_mustache_template").html();
                var template = render_template(cat_template, data);
                $("#id_search_filter_category_panel").html(template);
            },
            function (jqxhr, status, error) {
                
            },
            function (msg) {

            });
        }
    });

});
