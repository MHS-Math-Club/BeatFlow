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
            let accelHist = []
            let avgHist = []
            let direction = true
            let timeHist = []
            let longAccelHist = []
            console.log("accelerometer permission granted");
            var headingElementEnergy = document.getElementById("energy_value");
            var headingElement = document.getElementById("accel_value");
            var headingElementCadence = document.getElementById("cadence_value")

            function processMotionEvent(event) {
                var netAccel = Math.sqrt(event.acceleration.x ** 2 + event.acceleration.y ** 2 + event.acceleration.z ** 2);
                let parsed = parseFloat(netAccel.toFixed(1));
                headingElement.textContent = "Acceleration: " + parsed;
                
                //acceleration smoothing
                if (accelHist.length() > 100) {
                    accelHist.shift();
                }
                accelHist.push(netAccel);
                let avgAccel = accelHist.reduce(adder) / accelHist.length;

                function adder(total, value, index, array){
                    return total + value;
                }

                if (avgHist.length() > 100) {
                    avgHist.shift();
                }
                avgHist.push(avgAccel)
                
                //detect peaks
                if((avgHist[0] < avgHist[avgHist.length - 1] != direction) && (Math.abs(avgHist[0] - avgHist[avgHist.length - 1]) > 1)){
                    direction =  !direction;
                    longAccelHist.push(netAccel)
                }
                
                //finding cadence frequency
                if (timeHist.length() > 30){
                    timeHist.shift();
                }
                timeHist.push(new Date().getTime());
                let tdiffHist = [0]
                for(i = 1; i < timeHist.length; i++){
                    tdiffHist[i] = timeHist[i] - timeHist[i - 1];
                }

                avgDiff = tdiffHist.reduce(adder) / tdiffHist.length();

                cadence = 60000 / avgDiff;
                headingElementCadence.textContent = "Cadence: " + cadence;

                //Calculate energy
                if (longAccelHist.length > 30){
                    longAccelHist.shift();
                }
                var energy = cadence * 0.05 * longAccelHist.reduce(adder) / accelHist;
                headingElementEnergy.textContent = "Energy: " + energy;

                // Set another timeout for the next event processing after 100 milliseconds
            }

            // Add an event listener for the initial devicemotion event
            window.addEventListener('devicemotion', processMotionEvent);
        } else {
            headingElement.textContent = "Permission not granted";
        }
        });
    }