// JavaScript to show/hide the genre select dropdown
const genreDropdown = document.getElementById('genreDropdown');
const genreSelect = document.getElementById('genreSelect');
let energy = 0;
let netAccel = 0;

// JavaScript function
function openPopup() {
    var popup = document.getElementById("popup");
    popup.style.display = "flex";
}

function closePopup() {
    var popup = document.getElementById("popup");
    popup.style.display = "none";
    // Store a flag in localStorage to indicate that the popup has been closed
   localStorage.setItem('popupClosed', 'true');
}

document.addEventListener("DOMContentLoaded", function() {
    var form = document.getElementById("genre-form");
    
    form.addEventListener("change", function() {
        // Submit the form when any form element changes
        form.submit();
    });
});

window.onload = function() {
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

document.addEventListener('DOMContentLoaded', function() {
    const genreSelect = document.getElementById('genreSelect');
    const genreDropdown = document.getElementById('genreDropdown');

    genreSelect.addEventListener('change', function() {
        const selectedGenre = genreSelect.value;
        genreDropdown.textContent = selectedGenre;
        genreSelect.classList.add('d-none');
    });
});

var maxDataPoints = 200; // Adjust this number as needed
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

function throttle(func, delay) {
    let lastCall = 0;
    return function(...args) {
        const now = Date.now();
        if (now - lastCall >= delay) {
            lastCall = now;
            func(...args);
        }
    };
}

function Compute() {
    DeviceMotionEvent.requestPermission().then(response => {
        if (response == 'granted') {
            let accelHist = []
            let avgHist = [0, 0, 0]
            let timeHist = [0]
            let cadence = 0
            var headingElementAccel = document.getElementById("accel_value");
            var headingElementCadence = document.getElementById("cadence_value");

            function processMotionEvent(event) {
                var netAccel = Math.round(Math.sqrt(event.acceleration.x ** 2 + event.acceleration.y ** 2 + event.acceleration.z ** 2));
                let i = 0;
                headingElementAccel.textContent = "Acceleration: " + netAccel;

                //acceleration smoothing
                if (accelHist.length > 20) {
                    avgAccel = accelHist.reduce((a, b) => a + b) / accelHist.length;
                    accelHist.shift()
                    
                    if (avgHist.length > 20) {
                        avgHist.shift();
                    }
                    avgHist.push(avgAccel)

                    //peak detection
                    if((avgHist[0] + 0.3 < avgHist[Math.floor(avgHist.length / 2)] && avgHist[avgHist.length - 1] + 0.3 < avgHist[Math.floor(avgHist.length / 2)]) ){
                        
                        pTime = new Date().getTime();
                        if(pTime - timeHist[timeHist.length - 1] > 80){
                            console.log('Peak detected at average acceleration: ' + avgHist[Math.floor(avgHist.length / 2)])
                            //log times
                            if (timeHist.length > 20){
                                timeHist.shift();
                            }
                        
                            timeHist.push(pTime);
                            let tdiffHist = [0];
                            for(i = 1; i < timeHist.length; i++){
                                tdiffHist[i] = timeHist[i] - timeHist[i - 1];
                            }
    
                            avgDiff = tdiffHist.reduce((a, b) => a + b) / tdiffHist.length;
    
                            cadence = 60000 / avgDiff;
                            headingElementCadence.textContent = "Cadence: " + cadence;
                        }
                    }
                }
                

                accelHist.push(netAccel);              
                
                if (netAccel < 1) {
                    updateChart(netAccel * 10)
                } else {
                    updateChart(netAccel)
                }

            }

        // Add an event listener for the initial devicemotion event
        const throttledProcessMotionEvent = throttle(processMotionEvent, 1000);
        window.addEventListener('devicemotion', processMotionEvent);
        } else {
            headingElement.textContent = "Permission not granted";
        }
        });
    }

