document.addEventListener("DOMContentLoaded", function(event) {

    $('.custom-radio').on('click', function(e) {
        $(this).siblings('.custom-radio').each(function() {
            $(this).attr('class', 'custom-radio modal-selection');
            $(this).find('.custom-radio-circle').attr('class', 'custom-radio-circle');

        })

        $(this).attr('class', 'custom-radio modal-selection active-radio');
        $(this).find('.custom-radio-circle').attr('class', 'custom-radio-circle active-radio-circle');

    })

    $('.menu-selection').on('click', function() {
        $('.menu-selection .menu-selection-bottom').removeClass('selection-active');
        $(this).find('.menu-selection-bottom').addClass('selection-active');
    });

    $(this).on('click', '.status-message-close-button', function() {
        $(this).parent().hide();
    });


    $('.search-input').focus(function() {
        $(this).siblings('.search-dropdown').slideDown(300);
    })

    $('.search-input').focusout(function() {
        $(this).siblings('.search-dropdown').slideUp(300);
    });

    $('.search-option').on('click', function() {
        console.log($(this).parent().parent())
        $(this).parent().parent().siblings('.search-input').val($(this).text());
    })

    $('.search-input').on('input', function() {
        var matchingOptions = 0
        var searchText = $(this).val().toLowerCase();

        $(this).siblings('.search-dropdown').children().children().each(function() {
          var optionText = $(this).text().toLowerCase();
          if (optionText.indexOf(searchText) !== -1) {
            $(this).show();
            matchingOptions++;
          } else {
            $(this).hide();
          }
          if (matchingOptions == 0) {
            $('.no-results-option').show();
          } else {
            $('.no-results-option').hide();
          }
        });
      });

      $('.user-info').on('click', function(e) {
        $('.profile-info-wrapper').toggle();
    })

    $('.action-alert-exit').on('click', function() {
      $(this).parent().fadeOut(400);
  });
});



  