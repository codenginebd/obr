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
    
    function update_browser_address(search_params) {
        var url_address = "";
        for(var key in search_params) {
            if(url_address != "") {
                url_address += "&" + key + "=" + search_params[key];
            }
            else {
                url_address += key + "=" + search_params[key];
            }
        }
        window.history.pushState(search_params, "", url_address);
    }
    function collect_search_params(page) {
        var data = {};
        if(typeof page != "undefined") {
            data["page"] = page;
        }
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
        if(!sf_rating.isEmpty() && !sf_rating.isBlank()) {
            data["rating"] = sf_rating;
        }
        if(!sf_by_used.isEmpty() && !sf_by_used.isBlank()) {
            data["used"] = sf_by_used;
        }
        if(!sf_by_print.isEmpty() && !sf_by_print.isBlank()) {
            data["print"] = sf_by_print;
        }
        return data;
    }

    function perform_search(page) {
        var search_params = collect_search_params(page);
        update_browser_address(search_params);
        $("#id_search_results_pagination1").html("<p class='loading'>Loading...</p>");
        $("#id_search_results_pagination2").html("<p class='loading'>Loading...</p>");
        $("#id_search_results").html("<p class='loading'>Loading...</p>");
        call_ajax("GET", "/api/v1/books/", search_params, function (data) {
            //console.log(data);
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

    setTimeout(perform_search, 500);

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
                        //console.log(template);
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


    function search_action_handler(e) {
          e.preventDefault();
          var page = $(this).data("page");
          perform_search(page);
    }


    $(document).on("click", ".search-result-pager-item", function (e) {
        search_action_handler(e);
    });


});
