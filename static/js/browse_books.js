$(document).ready(function () {
    $(".book_entry_content").hover(function (e) {
        $(this).addClass("browse_item_hover");
        $(this).parent(".book_entry").addClass("browse_item_hover_color");
        $(this).find(".book_entry_action").removeClass("displaynone");
        $(this).find(".action-bar").slideDown("fast");
    }, function (e) {
        $(this).removeClass("browse_item_hover");
        $(this).parent(".book_entry").removeClass("browse_item_hover_color");
        $(this).find(".book_entry_action").addClass("displaynone");
        $(this).find(".action-bar").slideUp("fast");
    });

    $(".product-quick-view").click(function (e) {
        e.preventDefault();
        //alert("adsa");
        $("#product_view").modal('show');
        return false;
    });
    $(document).on("mousein", ".book_entry", function (e) {
        $(this).addClass("browse_item_hover");
    });
    $(document).on("mouseout", ".book_entry", function (e) {
        $(this).removeClass("browse_item_hover");
    });
    $('[data-toggle="tooltip"]').tooltip();
})