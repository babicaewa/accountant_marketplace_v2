var fadeSpeed = 200

document.addEventListener("DOMContentLoaded", function(event) {

    $('#loginFormButton').on('click', function() {
        $(this).attr("class", "classic-button");
        $('#signupFormButton').attr("class", "classic-button-inverse");
        $('#signupWrapper').fadeOut(fadeSpeed, function() {
            $('#loginWrapper').fadeIn(fadeSpeed);
        });
    });

    $('#loginLink').on('click', function() {
        $('#loginFormButton').attr("class", "classic-button");
        $('#signupFormButton').attr("class", "classic-button-inverse");
        $('#signupWrapper').fadeOut(fadeSpeed, function() {
            $('#loginWrapper').fadeIn(fadeSpeed);
        });
    });

    $('#signupFormButton').on('click', function() {
        $(this).attr("class", "classic-button");
        $('#loginFormButton').attr("class", "classic-button-inverse");
        $('#loginWrapper').fadeOut(fadeSpeed, function() {
            $('#signupWrapper').fadeIn(fadeSpeed);
        });
    });

    $('#signupLink').on('click', function() {
        $('#signupFormButton').attr("class", "classic-button");
        $('#loginFormButton').attr("class", "classic-button-inverse");
        $('#loginWrapper').fadeOut(fadeSpeed, function() {
            $('#signupWrapper').fadeIn(fadeSpeed);
        });
    });

  });