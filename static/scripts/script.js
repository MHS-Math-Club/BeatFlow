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
            let avgHist = [0, 0, 0]
            let direction = true
            let timeHist = []
            let longAccelHist = [1, 1]
            let cadence = 0
            console.log("accelerometer permission granted");
            var headingElementEnergy = document.getElementById("energy_value");
            var headingElement = document.getElementById("accel_value");
            var headingElementCadence = document.getElementById("cadence_value")

            function processMotionEvent(event) {
                var netAccel = Math.sqrt(event.acceleration.x ** 2 + event.acceleration.y ** 2 + event.acceleration.z ** 2);
                let parsed = parseFloat(netAccel.toFixed(1));
                headingElement.textContent = "Acceleration: " + parsed;

                //acceleration smoothing
                if (accelHist.length > 1000) {
                    accelHist.shift();
                }
                accelHist.push(netAccel);
                let avgAccel = accelHist.reduce(adder) / accelHist.length;

                function adder(total, value, index, array){
                    return total + value;
                }

                if (avgHist.length > 1000) {
                    avgHist.shift();
                }
                avgHist.push(avgAccel)
                
                //detect peaks
                if((avgHist[0] < avgHist[Math.floor(avgHist.length / 2)] && avgHist[avgHist.length] < avgHist[Math.floor(avgHist.length / 2)]) ){
                    longAccelHist.push(netAccel)
                    warn('Peak detected')
                    if (timeHist.length > 5){
                        timeHist.shift();
                    }
                    timeHist.push(new Date().getTime());
                    let tdiffHist = [0]
                    for(i = 1; i < timeHist.length; i++){
                        tdiffHist[i] = timeHist[i] - timeHist[i - 1];
                    }

                    avgDiff = tdiffHist.reduce(adder) / tdiffHist.length;

                    cadence = 60000 / avgDiff;
                    headingElementCadence.textContent = "Cadence: " + cadence;
                }
                //Calculate energy
                if (longAccelHist.length > 10){
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

function getNewSong(songList, idealTempo, idealEnergy, previousSongs){
    let bestSong = songList[0];
    let bestScore = 0;
    for(i = 0; i < songList.length; i++){
        let score = (Math.abs(adjustTempo(songList[i].tempo) - idealTempo)) + 0.3 * (Math.abs(songList[i].energy * 100 - idealEnergy));
        if(previousSongs.includes(songList[i].id)){
            score = 0;
        }
        if(score > bestScore){
            bestSong = songList[i];
            bestScore = score
        }
        
    }
    return bestSong.id;
}

function adjustTempo(tempo, cadence){
    let possibleTempos = [tempo / 4, tempo / 2, tempo, tempo * 2, tempo * 4]
    possibleTempos.sort(function(a){return Math.abs(a - cadence)})
    return possibleTempos[4]
    possibleTempos.sort(function(a, b){return Math.abs(a - cadence) - Math.abs(b - cadence)})
    return possibleTempos[0]
}