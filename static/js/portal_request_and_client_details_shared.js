document.addEventListener("DOMContentLoaded", function(event) {

    $('.menu-selection').on('click', function() {

        $('.deal-section').each(function() {
            $(this).hide();
        });

        var clickedSectionID = $(this).attr('id');

        switch (clickedSectionID) {
            case 'actionsNeededSelection':
                $('#actionsNeededSection').fadeIn(200);
                break;
            
            case 'documentsSelection':
                $('#documentsSection').fadeIn(200);
                break;

            case 'chatSelection':
                $('#chatSection').fadeIn(200);
                break;
            
            case 'serviceDetailsSelection':
                $('#serviceDetailsSection').fadeIn(200);
                break;
            
            case 'notesSelection':
                $('#notesSection').fadeIn(200);
                break;

        };
    })
});