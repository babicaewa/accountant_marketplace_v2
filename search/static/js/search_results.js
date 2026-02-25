function updateSliderBackground($slider) {
    const max = $slider.attr('max');
    const val = $slider.val();
    const radius_text = $('#radius-value');
    radius_text.val(val);
    radius_text.text(val + " km");
    const percentage = (val / max) * 100;
    $slider.css('--value', `${percentage}%`);
}

document.addEventListener("DOMContentLoaded", function(event) {

    $('.slider').each(function () {
        updateSliderBackground($(this));
        $(this).on('input', function () {
            updateSliderBackground($(this));
      });
    });

    $('#advancedSearchButton').on('click', function() {
        $('#advancedSearch').slideToggle(500, 'easeOutCubic')
        $('#plus').toggle();
        $('#minus').toggle();
    });

    $('#filterDropdown').on('click', function() {
        $('#filterDropdownMenu').toggle();
    });

    $('.dropdown-option').on('click', function() {
        if (!$(this).hasClass('search-option')) {
            var newVal = $(this).text();
            $('#filterDropdownVal').text(newVal);
            $('#filterDropdownMenu').toggle();
        }
    });
});

  