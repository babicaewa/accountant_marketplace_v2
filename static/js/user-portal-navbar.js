document.addEventListener("DOMContentLoaded", function(event) {

    $('.mobile-nav-toggle').on('click', function() {
        $('.navbar-overlay').toggle();
        $('.navbar-wrapper').toggle('slide');
        $('body').toggleClass('no-scroll');
    });

    $('.navbar-overlay').on('click', function() {
        $('.navbar-wrapper').toggle('slide');
        $('body').toggleClass('no-scroll');
        $('.navbar-overlay').toggle();
    });

    $(window).resize(function() {
        let moblieMaxWidth = 992;
        $('.navbar-overlay').css('display', 'none');

        if ($(window).width() > moblieMaxWidth) {
            $('.navbar-wrapper').css('display', 'flex');
        } else {
            $('.navbar-wrapper').css('display', 'none');
        }
    });

});

  