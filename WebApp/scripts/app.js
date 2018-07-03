var led_image = document.getElementById("led_image");
var led_label = document.getElementById("led_label");
var led_reference = firebase.database().ref().child('led');
var sensor_image = document.getElementById("sensor_image");
var sensor_label = document.getElementById("sensor_label");
var sensor_reference = firebase.database().ref().child('sensor');
var led_state;
var sensor_state;

function init(){
    console.log("Welcome to Domotrix");
    getLedData();
    getSensorData();
}

function toggleLed(){
    led_state = (led_state == "on")?"off":"on";
    console.log("The state of the led is: ", led_state);
    led_reference.update({state:led_state});
}

function getLedData(){
    led_reference.on('value', function(datasnapshot){
        led_state = datasnapshot.val().state;
        led_label.innerText = "State: "+led_state;
        led_image.src = "assets/led_"+led_state+".png";
    })
}

function getSensorData(){
    sensor_reference.on('value', function(datasnapshot){
        sensor_state = datasnapshot.val().state;
        sensor_label.innerText = "State: "+sensor_state;
        sensor_image.src = "assets/sensor_"+sensor_state+".png";
    })
}

window.onload = init;