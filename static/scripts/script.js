// JavaScript to show/hide the genre select dropdown
const genreDropdown = document.getElementById('genreDropdown');
const genreSelect = document.getElementById('genreSelect');
let energy = 0;
let netAccel = 0;

// Function to open the popup
function openPopup() {
    var popup = document.getElementById("popup");
    popup.style.display = "flex";
}

// Function to close the popup
function closePopup() {
    var popup = document.getElementById("popup");
    popup.style.display = "none";
    // Store a flag in localStorage to indicate that the popup has been closed
    localStorage.setItem('popupClosed', 'true');
}

document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("genre-form");

    form.addEventListener("change", function () {
        // Submit the form when any form element changes
        form.submit();
    });
});

window.onload = function () {
    var popupClosed = localStorage.getItem('popupClosed');
    if (!popupClosed) {
        openPopup();
    }
}

document.addEventListener('DOMContentLoaded', function () {
    var genreDropdown = document.getElementById('genreDropdown');
    var genreSelect = document.getElementById('genreSelect');

    genreDropdown.addEventListener('click', function () {
        genreSelect.classList.toggle('d-none');
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const genreSelect = document.getElementById('genreSelect');
    const genreDropdown = document.getElementById('genreDropdown');

    genreSelect.addEventListener('change', function () {
        const selectedGenre = genreSelect.value;
        genreDropdown.textContent = selectedGenre;
        genreSelect.classList.add('d-none');
    });
});

var maxDataPoints = 200; // Adjust this number as needed

// Function to update the chart
function updateChart(newValue) {
    // Add a new data point to the chart
    myChart.data.datasets[0].data.push(newValue);

    // If you want to add labels for each data point (e.g., timestamps)
    myChart.data.labels.push(new Date().toLocaleTimeString());
    console.log(myChart.data.datasets[0].data.length)

    // Remove the oldest data point if the limit is reached
    if (myChart.data.datasets[0].data.length > maxDataPoints) {
        myChart.data.datasets[0].data = [];
        myChart.data.labels = [];
    }

    myChart.update();
}

function Compute() {
    DeviceMotionEvent.requestPermission().then(response => {
        if (response == 'granted') {
            var headingElementAccel = document.getElementById("accel_value");

            function processMotionEvent(event) {
                var netAccel = Math.sqrt(event.acceleration.x ** 2 + event.acceleration.y ** 2 + event.acceleration.z ** 2);
                let parsed = Math.round(parseFloat(netAccel.toFixed(1)));
                let i = 0;
                headingElementAccel.textContent = "Acceleration: " + parsed;

                if (parsed < 1) {
                    updateChart(parsed * 10)
                } else {
                    updateChart(parsed)
                }

            }

            // Add an event listener for the initial devicemotion event
            window.addEventListener('devicemotion', processMotionEvent);
        } else {
            headingElement.textContent = "Permission not granted";
        }
    });
}


