document.addEventListener('DOMContentLoaded', function() {
  var socket = io.connect();
  socket.on("updateSensor1", function (msg) {
    Sensor1.innerHTML = msg;
    console.log(msg);
  });
});
