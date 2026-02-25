document.addEventListener("DOMContentLoaded", function(event) {

    $(document).on('input', '#documentSearchInput', function() {
        var matchingOptions = 0
        var searchText = $(this).val().toLowerCase();

        $('.document-wrapper').each(function() {
        var optionText = $(this).children('.document-name').children('.document-name-text').text().toLowerCase();
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

    $(document).on('click', '.view-document-button', function() {
        var filePath = $(this).data('file-path');
        window.open(filePath, '_blank');
    })
});