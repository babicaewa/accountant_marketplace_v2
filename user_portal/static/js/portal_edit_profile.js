function createLangaugeTag(langaugeName) {
    return $("<div class='language-tag-wrapper'><div class='tag language-tag'>" + langaugeName + "</div><div class='delete-button shadow-lg'><i class='bi bi-x'></i></div></div>");
}

document.addEventListener("DOMContentLoaded", function(event) {

    var pickedLanguages = document.querySelectorAll('.language-tag');
    var pickedLanguagesArr = Array.from(pickedLanguages).map(el => el.getAttribute('data-language'));
    $('#allSpokenLanguagesInput').val(pickedLanguagesArr);


    $(document).on('mouseenter', '.language-tag-wrapper', function() {
        $(this).find('.delete-button').css("display", "flex");
    });
    
    $(document).on('mouseleave', '.language-tag-wrapper', function() {
        $(this).find('.delete-button').css("display", "none");
    });

    $(document).on('click', '.search-input', function() {
        var matchingOptions = 0
        $(this).siblings('.search-dropdown').children().children().each(function() {
            var optionText = $(this).text().toLowerCase();
            if (pickedLanguagesArr.every(item => !item.includes($(this).text()))) {
  
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

      $(document).on('input', '.search-input', function() {
        var matchingOptions = 0
        var searchText = $(this).val().toLowerCase();

        $(this).siblings('.search-dropdown').children().children().each(function() {
          var optionText = $(this).text().toLowerCase();
          if (optionText.indexOf(searchText) !== -1 && pickedLanguagesArr.every(item => !item.includes($(this).text()))) {

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

      $(document).on('click', '.search-option', function() {
        $(this).parent().parent().siblings('.search-input').val("");
        selectedLanguageDiv = createLangaugeTag($(this).text());
        $('#allLanguagesWrapper').append(selectedLanguageDiv);
        pickedLanguagesArr.push($(this).text());
        $('#allSpokenLanguagesInput').val(pickedLanguagesArr);
    })

    $(document).on('click', '.language-tag-wrapper', function() {
      $(this).remove();
      pickedLanguagesArr = pickedLanguagesArr.filter(language => language !== $(this).text().trim());
      $('#allSpokenLanguagesInput').val(pickedLanguagesArr);
    });

    $(document).on('click', '#newExperienceButton', function() {
      $('#addExperienceForm')[0].reset();
      $('#experienceID').val("");
    })

    $(document).on('click', '.edit-experience-button', function() {
      var experienceDiv = $(this).parent().siblings('.experience-title');
      var experienceID = experienceDiv.children('.experience-id').data('experience-id');
      var role = experienceDiv.children('.experience-role').text();
      var companyName = experienceDiv.children('.experience-company').children('.experience-company-name').text();
      var startDate = experienceDiv.children('.experience-date').children('.experience-start-year').text();
      var endDate = experienceDiv.children('.experience-date').children('.experience-end-year').text();

      var focus = $(this).parent().parent().siblings('.experience-focus').children('.experience-focus-text').text();
      
      $('.experience-focus-text').text();

      $('#experienceID').val(experienceID);
      $('#jobTitleInput').val(role);
      $('#companyInput').val(companyName);
      $('#startYearInput').val(startDate);
      if (!isNaN(endDate)) {
        $('#endYearInput').val(endDate);
      } else {
        $('#endYearInput').val("");
      }
      $('#workFocusInput').val(focus.trim());
    })

});