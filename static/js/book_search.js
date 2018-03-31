$(document).ready(function () {
   $(document).on("click", ".btn-browse-filter", function (e) {
        e.preventDefault();
        $("#id_browse_more_filter_content").slideToggle(500);
    });
    
    function update_browser_address() {
        
    }
    
    function collect_search_params() {
        
    }

    function perform_search() {
        var search_params = collect_search_params();
        update_browser_address();
        $("#id_search_results_pagination1").html("<p class='loading'>Loading...</p>");
        $("#id_search_results_pagination2").html("<p class='loading'>Loading...</p>");
        $("#id_search_results").html("<p class='loading'>Loading...</p>");
        call_ajax("GET", "/api/v1/books/", search_params, function (data) {
            var pagination_template = $("#id_search_pagination_hb_template").html();

            var pagination_object = Pager.create_pagination_object(data.length, 3, 2, 10);
            var pagination_rendered = render_template(pagination_template, pagination_object);
            $("#id_search_results_pagination1").html(pagination_rendered);
            $("#id_search_results_pagination2").html(pagination_rendered);

            var search_result_template = $("#id_search_results_hb_template").html();
            var rendered_results = render_template(search_result_template, {"results": data});
            $("#id_search_results").html(rendered_results);
        },
        function (jqxhr, status, error) {
            
        },
        function (msg) {
            
        });
    };

    setTimeout(perform_search, 1000);

    $(document).on("click", ".search-filter-by-category", function (e) {
        if($(this).is(":checked")) {
            var parent_cat_id = $(this).val();
            call_ajax("GET", "/api/v1/categories/", { "pid": parent_cat_id },
            function (data) {
                var cat_template = $("#id_search_category_mustache_template").html();
                var template = render_template(cat_template, data);
                $("#id_search_filter_category_panel").html(template);


                call_ajax("GET", "/api/v1/authors/", { "cid": parent_cat_id },
                    function (data) {
                        var author_template = $("#id_search_author_mustache_template").html();
                        var template = render_template(author_template, data);
                        console.log(template);


                    },
                    function (jqxhr, status, error) {

                    },
                    function (msg) {

                    });


            },
            function (jqxhr, status, error) {
                
            },
            function (msg) {

            });
        }
    });

    $(document).on("click", ".filter_search_prev_cat", function (e) {
        call_ajax("GET", "/api/v1/category-browse/", { "pid": $(this).val() },
            function (data) {
                var cat_template = $("#id_search_category_mustache_template").html();
                var template = render_template(cat_template, data);
                $("#id_search_filter_category_panel").html(template);
                e.preventDefault();
            },
            function (jqxhr, status, error) {

            },
            function (msg) {

            });
    });

});
