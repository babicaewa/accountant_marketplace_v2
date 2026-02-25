function updateDirectory(id) {
    var directoryID = id +'-checkpoint';
    $('.checkpoint').each(function() {
        var text = $(this).find('.directory-link');
        if ($(this).attr('id') == directoryID) {
            text.css('color', 'var(--secondary-color-20)');
        }
        else {
            text.css('color', 'black');
        }
    });
}


document.addEventListener("DOMContentLoaded", function(event) {

    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

    
    $(window).on('scroll', function() {
        $('.content-section').each(function() {
            const rect = $(this)[0].getBoundingClientRect();
            const isVisible = rect.top < window.innerHeight && rect.bottom > 100;
        
            if (isVisible) {
              var visibleSection = $(this).attr('id');
              updateDirectory(visibleSection);
              return false; 
            }
          });
    });
    
    var user_location = $('#map').data("lat_long");
    var user_location_lat_long = user_location.split(",");
    var map = L.map('map').setView([user_location_lat_long[0], user_location_lat_long[1]], 17);
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
    var marker = L.marker([user_location_lat_long[0], user_location_lat_long[1]]).addTo(map);
    var user_address = $('#map').data("address");
    marker.bindPopup("<a href='https://www.google.com/maps/place/" + user_address + "' target='_blank'>" + user_address +"</a>").openPopup();


    $('.service-checkbox').on('click', function() {
        console.log("waaa")
        var quantityWrapper = $(this).siblings('.quantity-wrapper');
        quantityWrapper.toggleClass('active');
    })

  });