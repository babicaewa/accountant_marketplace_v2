document.addEventListener("DOMContentLoaded", function(event) {
    $('.billing-details-toggle').on('click', function() {
        $(this).siblings('.billing-details-content').slideToggle();
    })
});
