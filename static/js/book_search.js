String.prototype.isEmpty = function() {
    return (this.length === 0 || !this.trim());
};

String.prototype.isBlank = function() {
    return (!this || /^\s*$/.test(this));
};

$(document).ready(function () {
   $(document).on("click", ".btn-browse-filter", function (e) {
        e.preventDefault();
        $("#id_browse_more_filter_content").slideToggle(500);
    });
    
    function update_browser_address(search_params) {
        var url_address = "?";
        for(var key in search_params) {
            if(url_address != "?") {
                url_address += key + "=" + search_params[key] + "&";
            }
            else {
                url_address += key + "=" + search_params[key] + "&";
            }
        }
        if(url_address != "?") {
            url_address = url_address.substr(0, url_address.length - 1);
        }
        window.history.pushState(search_params, "", url_address);
    }
    function collect_search_params(page) {
        var data = {};
        var page = $("input[name=sf-current-page]").val();
        var sf_isbn = $("input[name=sf-isbn]").val();
        var sf_keyword = $("input[name=sf-keyword]").val();
        var sf_bl = "";
        var sf_rating = "";

        var bl_values = [];
        $('input[name=sf-bl]:checked').each(function(index, elem) {
            bl_values.push($(elem).val());
        });
        sf_bl = bl_values.join(',');

        var rating_values = [];
        $('input[name=sf-rating]:checked').each(function(index, elem) {
            rating_values.push($(elem).val());
        });
        sf_rating = rating_values.join(',');

        var sf_by_used = "";

        var by_used_values = [];
        $('input[name=sf-by-used]:checked').each(function(index, elem) {
            by_used_values.push($(elem).val());
        });
        sf_by_used = by_used_values.join(',');

        var sf_by_print = "";

        var by_print_values = [];
        $('input[name=sf-by-print]:checked').each(function(index, elem) {
            by_print_values.push($(elem).val());
        });
        sf_by_print = by_print_values.join(',');

        if($("input[name=sf-out-of-stock]").is(":checked")) {
            data["out-of-stock"] = 0
        }

        if(typeof page != "undefined" && !page.isEmpty() && !page.isBlank()) {
            try {
                page = parseInt(page);
            }catch(err) {
                page = null;
            }
            if(page != null) {
                data["page"] = page;
            }
        }
        if(typeof sf_isbn != "undefined" && !sf_isbn.isEmpty() && !sf_isbn.isBlank()) {
            data["isbn"] = sf_isbn;
        }
        if(typeof sf_keyword != "undefined" && !sf_keyword.isEmpty() && !sf_keyword.isBlank()) {
            data["keyword"] = sf_keyword;
        }
        if(typeof sf_bl != "undefined" && !sf_bl.isEmpty() && !sf_bl.isBlank()) {
            data["lang"] = sf_bl;
        }
        if(typeof sf_rating != "undefined" && !sf_rating.isEmpty() && !sf_rating.isBlank()) {
            data["rating"] = sf_rating;
        }
        if(typeof sf_by_used != "undefined" && !sf_by_used.isEmpty() && !sf_by_used.isBlank() && sf_by_used != "any") {
            data["use-status"] = sf_by_used;
        }
        if(typeof sf_by_print != "undefined" && !sf_by_print.isEmpty() && !sf_by_print.isBlank() && sf_by_print != "any") {
            data["print-type"] = sf_by_print;
        }

        var category_values = [];
        $('input[name=search-filter-by-category]:checked').each(function(index, elem) {
            category_values.push($(elem).val());
        });
        var category = category_values.join(',');

        if(typeof category != "undefined" && !category.isEmpty() && !category.isBlank()) {
            data["cat"] = category;
        }

        var author_values = [];
        $('input[name=filter-author-name]:checked').each(function(index, elem) {
            author_values.push($(elem).val());
        });
        var author = author_values.join(',');

        if(typeof author != "undefined" && !author.isEmpty() && !author.isBlank()) {
            data["author"] = author;
        }

        var publisher_values = [];
        $('input[name=filter-publisher]:checked').each(function(index, elem) {
            publisher_values.push($(elem).val());
        });
        var publishers = publisher_values.join(',');
        if(typeof publishers != "undefined" && !publishers.isEmpty() && !publishers.isBlank()) {
            data["publisher"] = publishers;
        }
        console.log(data);
        return data;
    }

    function perform_search(page) {
        var search_params = collect_search_params(page);
        console.log("Search params...");
        console.log(search_params);
        update_browser_address(search_params);
        $("#id_search_results_pagination1").html("<p class='loading'>Loading...</p>");
        $("#id_search_results_pagination2").html("<p class='loading'>Loading...</p>");
        $("#id_search_results").html("<p class='loading'>Loading...</p>");
        call_ajax("GET", "/api/v1/books/", search_params, function (data) {
            //console.log(data);
            var pagination_template = $("#id_search_pagination_hb_template").html();
            var current_page = -1;
            var prev_page = data.previous;
            var next_page = data.next;

            if(next_page != null) {
                var i = next_page.lastIndexOf("?");
                if(i != -1) {
                    var page_number = next_page.substr(i + 6, next_page.length);
                    if (page_number != null && page_number != "") {
                        current_page = parseInt(page_number) - 1;
                    }
                }
            }
            if(current_page == -1) {
                if(prev_page != null) {
                    var i = prev_page.lastIndexOf("?");
                    if(i != -1) {
                        var page_number = prev_page.substr(i + 6, prev_page.length);
                        if (page_number != null && page_number != "") {
                            current_page = parseInt(page_number) + 1;
                        }
                    }
                    else {
                        current_page = 2;
                    }
                }
            }

            if(current_page == -1) {
                current_page = 1;
            }

            var pagination_object = Pager.create_pagination_object(data.count, 10, current_page, 10);
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
          perform_search();
    }

    $(document).on("click", ".pagination-li-item", function (e) {
        var page = $(this).data("page");
        $("input[name=sf-current-page]").val(page);
        search_action_handler(e);
    });


    
    $(document).on("change", ".sr-rent-option", function (e) {
        e.preventDefault();
        var value = $(this).val();
        var new_item = true;
        if($(this).hasClass("new")) {
            new_item = true;
        }
        else if($(this).hasClass("used")) {
            new_item = false;
        }
        var parent_panel = $(this).closest(".panel-body").parent();
        var buy_cart_btn = $(parent_panel).find(".add-to-buy-cart");
        var price_currency_span = $(parent_panel).find(".sale-price-currency-span");
        var price_span = $(parent_panel).find(".sale-price-span");

        var product_code = $(this).closest(".book_entry").data("item-code");
        var product_type = $(this).closest(".book_entry").data("item-type");

        call_ajax("GET", "/api/v1/sale-price/", { "ptype": product_type, "pcode": product_code, "pr-type": value, "used": !new_item },
        function (data) {
            $(buy_cart_btn).prop("disabled", false);
            $(price_currency_span).text(data.currency_code);
            $(price_span).text(data.sale_price);
            $(price_currency_span).parent().removeClass("hidden");
        },
        function (jqxhr, status, error) {

        },
        function (msg) {

        });

    });

    $(document).on("keyup", "input[name=sf-isbn]", function (e) {
        if(e.keyCode == 13) {
            perform_search();
        }
    });

    $(document).on("keyup", "input[name=sf-keyword]", function (e) {
        if(e.keyCode == 13) {
            perform_search();
        }
    });

    $(document).on("change", "input[name=sf-bl]", function(e) {
        perform_search();
    });

    $(document).on("change", "input[name=sf-rating]", function(e) {
        perform_search();
    });

    $(document).on("change", "input[name=sf-by-used]", function(e) {
        perform_search();
    });

    $(document).on("change", "input[name=sf-by-print]", function(e) {
        perform_search();
    });

    $(document).on("change", "input[name=sf-out-of-stock]", function(e) {
        perform_search();
    });
    
    $(document).on("change", "input[name=search-filter-by-category]", function (e) {
        perform_search();
    });
    
    $(document).on("change", "input[name=filter-author-name]", function (e) {
        perform_search();
    });
    
    $(document).on("change", "input[name=filter-publisher]", function (e) {
        perform_search();
    });
});
