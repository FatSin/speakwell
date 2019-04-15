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