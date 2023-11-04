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
            console.log("accelerometer permission granted");
            window.addEventListener('devicemotion', (event) => {
                var headingElement = document.getElementById("accel_value");
                var netAccel = Math.sqrt(event.acceleration.x ** 2 + event.acceleration.y ** 2 + event.acceleration.z ** 2)
                let parsed = parseFloat(netAccel.toFixed(3));

                headingElement.textContent = netAccel.toString();
            })
        }
        else{
            headingElement.textContent = "Permission not granted"
        }
    });
}

function adjustTempo(tempo, cadence){
    let possibleTempos = [tempo / 4, tempo / 2, tempo, tempo * 2, tempo * 4]
    possibleTempos.sort(function(a){return Math.abs(a - cadence)})
    return possibleTempos[4]
}

function adjustSpeed(tempo, cadence){
    return cadence / adjustTempo(tempo, cadence)
}