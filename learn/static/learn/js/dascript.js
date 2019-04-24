function formValidate() {
    var formIndex, username, password, error;
    formIndex = document.getElementById('form-index');
    username = document.getElementByName("username").value;
    password = document.getElementByName("password").value;

    if (password.length < 8) {
        error = 'The password is too short';
        var formError = document.getElementById('form-error');
        formError.innerText = error;
        return false;
    }
}



function playAudio(filename) {
    var audio;
    audio = document.getElementById(filename);
    console.log(filename);
    audio.play();
}


function recordAudio(word, lang, wordinlang, word2) {

    var csrfcookie = function() {
        var cookieValue = null,
            name = 'csrftoken';
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };
  var start = document.getElementById('start-'+word);
  var stop = document.getElementById('stop-'+word);

    navigator.mediaDevices.getUserMedia({ audio: true, video: false })
        .then(function(mediaStreamObj) {
            /*
            if ("srcObject" in audio){
                audio.srcObject = mediaStreamObj;
            }
            else {
                audio.src = window.URL.createObjectURL(mediaStreamObj);
            }
            */
            var recorder = new MediaRecorder(mediaStreamObj);
            var chunks = [];


            /*
            start.addEventListener('click', function(e) {
                recorder.start();
                console.log(recorder.state);
            });
            */
            alert('Ready?')
            recorder.start();
            console.log(recorder.state);

            stop.addEventListener('click', function(e) {
                recorder.stop();
                console.log(recorder.state);
            });

            recorder.ondataavailable = function(e){
                chunks.push(e.data);
            }
            recorder.onstop = function(e){
                var blob = new Blob(chunks, {'type' : 'audio/mpeg-3' });
                /*
                var audioURL = window.URL.createObjectURL(blob);
                audio.src = audioURL;
                */
                var xhr = new XMLHttpRequest();
                xhr.open('POST', '/learn/storeaudio/', true);
                xhr.setRequestHeader('X-CSRFToken', csrfcookie());
                xhr.onload = function(e) {
                    //Callback
                    console.log('Sent');
                    //console.log(xhr.responseText);
                    //document.getElementById('div-voc').innerHTML = xhr.responseText;
                };
                xhr.send(blob);

                var xhr2 = new XMLHttpRequest();
                xhr2.open('POST', '/learn/record/', true);
                xhr2.setRequestHeader('X-CSRFToken', csrfcookie());
                var parameters = word+','+lang+','+wordinlang+','+word2;
                xhr2.onload = function(e) {
                    //Callback
                    console.log('Evaluation in progress');
                    console.log(word+','+lang+','+wordinlang+','+word2);
                    console.log(xhr2.responseText);
                    //document.getElementById('div-voc').innerHTML = xhr2.responseText;
                    document.body.innerHTML = xhr2.responseText;
                };
                xhr2.send(parameters);
            }
        })
        .catch(function(err){
            console.log(err.name, err.message);
        });
}