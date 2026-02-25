document.addEventListener("DOMContentLoaded", function(event) {

    $('#forumTagSearchInput').on('focus', function() {
        $('.tag-dropdown').css('display', 'flex');
    });

    $('#forumTagSearchInput').on('blur', function() {
        setTimeout(function() {
            $('.tag-dropdown').hide();
        }, 100);
    });

    $('#forumTagSearchInput').on('input', function() {
        var matchingTags = 0
        var searchText = $(this).val().toLowerCase();
        
        $('.tag-dropdown .tag').each(function() {
          var tagText = $(this).text().toLowerCase();
          if (tagText.indexOf(searchText) !== -1) {
            $(this).show();
            matchingTags++;
          } else {
            $(this).hide();
          }
          if (matchingTags == 0) {
            $('#noMatchingTags').show();
          } else {
            $('#noMatchingTags').hide();
          }
        });
      });
      
      $('.question-tag').on('click', function() {
        var clickedTag = $(this).clone();
        clickedTag.addClass('selected-tag');
        clickedTag.append('<i class="bi bi-x"></i>');
        $('#forumTagSearchInput').hide();
        $('.tag-search-input-wrapper').append(clickedTag);
      });

      $(document).on('click', '.selected-tag', function() {
        $(this).remove();
        $('#forumTagSearchInput').show();
      });

      $('#forumFilterDropdown').on('click', function() {
        $('#forumFilterDropdownMenu').toggle();
        });

    $('.dropdown-option').on('click', function() {
        var newVal = $(this).text();
        $('#forumFilterVal').text(newVal);
        $('#forumFilterDropdownMenu').toggle();
        })

  });