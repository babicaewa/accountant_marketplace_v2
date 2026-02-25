document.addEventListener("DOMContentLoaded", function(event) {
    var chatbox = $('.chatbox-content');

    $('.modal-selections-wrapper').on('click', function(e) {
        if($('#awaitingApprovalRadio').hasClass('active-radio')) {
            $('#approvalNote').show();
        } else {
            $('#approvalNote').hide();
        }
    }); 

    $(document).on('click', '.delete-file-button', function() {
        var filetToDeleteName = $(this).parent().siblings(".document-name-and-icon").find('.document-name').text();
        $('#fileToDeleteText').text(filetToDeleteName);
        $('#deleteFileName').val(filetToDeleteName);
    })
      
      $(document).on('htmx:afterRequest', function(event) {
        console.log(event.target)
        if ($(event.target).attr('id')== "fileUploadForm") {
            $(event.target).trigger('reset');
            $('#fileUpload').modal('hide');
            if(event.detail.successful) {
                $('#successUploadAlert').css("display", "flex").hide().fadeIn();
            } else {
                $('#failUploadAlert').css("display", "flex").hide().fadeIn();
            }
        } else if ($(event.target).attr('id')== "fileDeleteForm") {
            if(event.detail.successful) {
                $('#successDeleteAlert').css("display", "flex").hide().fadeIn();
            } else {
                $('#failDeleteAlert').css("display", "flex").hide().fadeIn();
            }
        } else if ($(event.target).attr('id')== "chatSection") {
            var chatbox = $('.chatbox-content');
            chatbox.scrollTop(chatbox[0].scrollHeight);
        }
      });  

    $('#editNotesButton').on('click', function() {
        $('#notesContent').toggle();
        $('#notesTextEditWrapper').toggle();
    });


    $('#chatSelection').on('click', function() {
        setTimeout(function() {
            chatbox.scrollTop(chatbox[0].scrollHeight);
        }, 100)
    })


})