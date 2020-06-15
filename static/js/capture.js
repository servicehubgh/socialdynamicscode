
$(document).ready(function () {
    let realtimeCapture = true;
    let cameraFront = true;
    let images= [];

    showCam();

    function showCam() {
        let setting;
        cameraFront = !cameraFront;
        if (cameraFront) {
            setting = {width: 640, height: 480, image_format: 'jpeg', jpeg_quality: 100};
        }
        else {
            setting = {width: 640, height: 480, image_format: 'jpeg', jpeg_quality: 100, facingMode: 'environment'};
        }
        Webcam.set('constraints', setting);
        Webcam.attach('#my_camera');
    }

    function snapCamera() {
        let num = images.length;
        if (realtimeCapture) {
            Webcam.snap(function (data_uri) {
                console.log(data_uri)
                return images.push(data_uri)});
            if (num < 10){
                $('#results').append(
                    '<img id="image" style="display: inline-block; margin-left: 20px; margin-bottom: 20px; float: left; ' +
                    'width: 160px ; height: 160px" src="' + images[num] + '"/>')}
            else
                realtimeCapture = false;
        }
    }

    $("#start-button").click(function () {
        setInterval(snapCamera, 1000)
    });
});

