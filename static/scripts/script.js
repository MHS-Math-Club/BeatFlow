// JavaScript to show/hide the genre select dropdown
const genreDropdown = document.getElementById('genreDropdown');
const genreSelect = document.getElementById('genreSelect');
let energy = 0;
let netAccel = 0;
let accelHist = []
let avgHist = [0, 0, 0]
let timeHist = []
let longAccelHist = [1, 1]
let cadence = 0

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

function calculateCadence(netAccel) {
    /// function
    if (accelHist.length > 50) {
        avgAccel = accelHist.reduce(adder) / accelHist.length;
        accelHist.shift()
        
        if (avgHist.length > 20) {
            avgHist.shift();
        }
    avgHist.push(avgAccel)
    }
    if((avgHist[0] + 0.3 < avgHist[Math.floor(avgHist.length / 2)] && avgHist[avgHist.length - 1] + 0.3 < avgHist[Math.floor(avgHist.length / 2)]) ){

        pTime = new Date().getTime();
        if(pTime - timeHist[timeHist.length] > 250){

            longAccelHist.push(netAccel)
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

            avgDiff = tdiffHist.reduce(adder) / tdiffHist.length;

            cadence = 60000 / avgDiff;
            
        }
    }
    return cadence;
}

// Function to create a cadence stream
function createCadenceStream(netAccel) {
  const cadenceStream = {
    onValue: function (callback) {
      const interval = 1000; // Interval in milliseconds
      setInterval(() => {
        const cadence = calculateCadence(netAccel);
        callback(cadence);
      }, interval);
    },
  };
  return cadenceStream;
}

function Compute() {
    DeviceMotionEvent.requestPermission().then(response => {
        if (response == 'granted') {
            var headingElementAccel = document.getElementById("accel_value");
            var headingElementCadence = document.getElementById("cadence_value");

            function processMotionEvent(event) {
                var netAccel = Math.sqrt(event.acceleration.x ** 2 + event.acceleration.y ** 2 + event.acceleration.z ** 2);
                let parsed = Math.round(parseFloat(netAccel.toFixed(1)));
                headingElementAccel.textContent = "Acceleration: " + parsed;

                if (parsed < 1) {
                    updateChart(parsed * 10);
                } else {
                    updateChart(parsed);
                }

                // Cadence calculation
                var cadenceStream = createCadenceStream(netAccel);
                cadenceStream.onValue(function(val) {
                    headingElementCadence.textContent = val;
                });

            }

            // Add an event listener for the initial devicemotion event
            window.addEventListener('devicemotion', processMotionEvent);
        } else {
            headingElementAccel.textContent = "Permission not granted";
        }
    });
}



