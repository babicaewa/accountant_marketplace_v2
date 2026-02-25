document.addEventListener("DOMContentLoaded", function(event) {

    $('.title-and-dropdown').on('click', function() {
        var content = $(this).siblings('.dropdown-content-section');
        var contentArrow = $(this).find('.title-dropdown');
        content.slideToggle(500, 'easeOutCubic');
        contentArrow.toggleClass('rotated');
    });

    
});