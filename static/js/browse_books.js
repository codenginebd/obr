$(document).ready(function () {
    $(".book_entry").hover(function (e) {
        $(this).addClass("opacity_08");
        $(this).find(".book_entry_action").removeClass("displaynone");
    }, function (e) {
        $(this).removeClass("opacity_08");
        $(this).find(".book_entry_action").addClass("displaynone");
    })
})