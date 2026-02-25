const chartColor = '#1c4e58';

document.addEventListener("DOMContentLoaded", function(event) {

    $('#daysDropdown').on('click', function() {
        $('#daysDropdownMenu').toggle();
    });

    $('.dropdown-option').on('click', function() {
        var newVal = $(this).text();
        $('#daysDropdownVal').text(newVal);
        $('#daysDropdownMenu').toggle();
    })

    const xValues = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


    new Chart("revenueChart", {
    type: "bar",
    data: {
        labels: xValues,
        datasets: [{ 
        data: [100,0,0,0,0,400,0,0,0,2000,0,0],
        backgroundColor: chartColor,
        fill: true,
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false,
            }
        },
        scales: {
            x: {
                grid: {
                    display: false
                },
            },
            y: {
                grid: {
                    display: false
                },
                ticks: {
                    // Include a dollar sign in the ticks
                    callback: function(value, index, ticks) {
                        return '$' + value;
                    }
                },
            }
        },
    }
    });
});

