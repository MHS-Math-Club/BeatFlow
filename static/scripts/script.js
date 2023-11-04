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

function getCadence(){
    console.log("JS loaded")
    DeviceMotionEvent.requestPermission().then(response => {
        if (response == 'granted') {
            let accelHist = []
            let avgHist = []
            let direction = true
            let timeHist = []
            console.log("accelerometer permission granted");
            window.addEventListener('devicemotion', (event) => {
                var headingElement = document.getElementById("accel_value");
                var netAccel = Math.sqrt(event.acceleration.x ** 2 + event.acceleration.y ** 2 + event.acceleration.z ** 2)
                let parsed = parseFloat(netAccel.toFixed(3));
                if (accelHist.length() > 30) {
                    accelHist.shift()
                }
                accelHist.push(netAccel)
                let avgAccel = accelHist.reduce(adder) / accelHist.length

                function adder(total, value, index, array){
                    return total + value
                }

                if (avgHist.length() > 30) {
                    avgHist.shift()
                }
                avgHist.push(avgAccel)
                if(avgHist[0] < avgHist[avgHist.length - 1] != direction){
                    direction =  !direction
                }

                if (timeHist.length() > 30){
                    timeHist.shift()
                }
                timeHist.push(new Date().getTime())
                let tdiffHist = [0]
                for(i = 1; i < timeHist.length; i++){
                    tdiffHist[i] = timeHist[i] - timeHist[i - 1]
                }

                avgDiff = tdiffHist.reduce(adder) / tdiffHist.length()

                cadence = 60000 / avgDiff
                
                headingElement.textContent = cadence.toString();
            })
        }
        else{
            headingElement.textContent = "Permission not granted"
        }
    });
}

function adjustTempo(tempo, cadence){
    let possibleTempos = [tempo / 4, tempo / 2, tempo, tempo * 2, tempo * 4]
    possibleTempos.sort(function(a, b){return Math.abs(a - cadence) - Math.abs(b - cadence)})
    return possibleTempos[0]
}

function adjustSpeed(tempo, cadence){
    return cadence / adjustTempo(tempo, cadence)
}