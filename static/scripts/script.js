// JavaScript to show/hide the genre select dropdown
const genreDropdown = document.getElementById('genreDropdown');
const genreSelect = document.getElementById('genreSelect');

genreDropdown.addEventListener('click', function () {
    genreSelect.classList.toggle('d-none');
});

genreSelect.addEventListener('change', function () {
    const selectedGenre = genreSelect.value;
    genreDropdown.textContent = selectedGenre;
    genreSelect.classList.add('d-none');
});

function getCadence() {
    console.log("JS loaded");
    DeviceMotionEvent.requestPermission().then(response => {
        if (response == 'granted') {
            console.log("accelerometer permission granted");
            var headingElementEnergy = document.getElementById("energy_value");
            var headingElement = document.getElementById("accel_value");

            function processMotionEvent(event) {
                var netAccel = Math.sqrt(event.acceleration.x ** 2 + event.acceleration.y ** 2 + event.acceleration.z ** 2);
                let parsed = parseFloat(netAccel.toFixed(1));
                headingElement.textContent = "Acceleration: " + parsed;

                let parsed30 = parseFloat(((parsed * 10 + 30)).toFixed(1));
                let parsed60 = parseFloat(((parsed + 60)).toFixed(1));
                let parsed90 = parseFloat(((parsed + 80)).toFixed(1));

                if (netAccel < 2) {
                    headingElementEnergy.textContent = "Energy: " + parsed30;
                } else if (netAccel > 2 && netAccel < 10) {
                    headingElementEnergy.textContent = "Energy: " + parsed60;
                } else {
                    headingElementEnergy.textContent = "Energy: " + parsed90;
                }

                // Set another timeout for the next event processing after 100 milliseconds
                setTimeout(processMotionEvent, 100);
            }

            // Add an event listener for the initial devicemotion event
            window.addEventListener('devicemotion', processMotionEvent);
        } else {
            headingElement.textContent = "Permission not granted";
        }
        });
    }