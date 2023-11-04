
accelReader = document.getElementsByID("accelReader");
function getCadence(){
    console.log("JS loaded")
    accelReader.innerHTML = "HTML modification works";
    DeviceMotionEvent.requestPermission().then(response => {
        if (response == 'granted') {
            console.log("accelerometer permission granted");
            window.addEventListener('devicemotion', (event) => {
                var netAccel = Math.sqrt(event.acceleration.x ** 2 + event.acceleration.y ** 2 + event.acceleration.z ** 2)
                
                window.alert(netAccel)
                accelReader.innerHTML = netAccel.toString()
            })

        }
        else{
            accelReader.innerHTML = "JS works!"
        }
    });
}