String.prototype.isEmpty = function() {
    return (this.length === 0 || !this.trim());
};

String.prototype.isBlank = function(str) {
    return (!str || /^\s*$/.test(str));
};

$(document).ready(function () {
   $(document).on("click", ".btn-browse-filter", function (e) {
        e.preventDefault();
        $("#id_browse_more_filter_content").slideToggle(500);
    });
    
    function update_browser_address() {
        
    }
    
    function collect_search_params() {
        var data = {};
        var sf_isbn = $("input[name=sf-isbn]").val();
        var sf_keyword = $("input[name=sf-keyword]").val();
        var sf_bl = $("input[name=sf-bl]").val();
        var sf_rating = $("input[name=sf-rating]").val();
        var sf_by_used = $("input[name=sf-by-used]").val();
        var sf_by_print = $("input[name=sf-by-print]").val();
        
        if(!sf_isbn.isEmpty() && !sf_keyword.isBlank()) {
            data["isbn"] = sf_isbn;
        }
        if(!sf_keyword.isEmpty() && !sf_keyword.isBlank()) {
            data["keyword"] = sf_keyword;
        }
        if(!sf_bl.isEmpty() && !sf_bl.isBlank()) {
            data["bl"] = sf_bl;
        }
        return data;
    }

    function perform_search() {
        var search_params = collect_search_params();
        update_browser_address();
        $("#id_search_results_pagination1").html("<p class='loading'>Loading...</p>");
        $("#id_search_results_pagination2").html("<p class='loading'>Loading...</p>");
        $("#id_search_results").html("<p class='loading'>Loading...</p>");
        call_ajax("GET", "/api/v1/books/", search_params, function (data) {
            console.log(data);
            var pagination_template = $("#id_search_pagination_hb_template").html();

            var pagination_object = Pager.create_pagination_object(data.count, 10, 1, 10);
            var pagination_rendered = render_template(pagination_template, pagination_object);
            $("#id_search_results_pagination1").html(pagination_rendered);
            $("#id_search_results_pagination2").html(pagination_rendered);

            var search_result_template = $("#id_search_results_hb_template").html();
            var rendered_results = render_template(search_result_template,data);
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
