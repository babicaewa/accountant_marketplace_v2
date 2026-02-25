document.addEventListener("DOMContentLoaded", function(event) {

    $('.client-ellipsis').on('click', function() {
        $(this).siblings('.remove-client-card').toggle();
    })
  });