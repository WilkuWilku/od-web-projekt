$(document).ready(() => {
    console.log('ddd');

    $('#signin-password-input').blur(() => {
        let strength = calculatePasswordStrength();
        let strengthText = '';
        let strengthClass = '';
        if(strength < 28) {
            strengthText = "bardzo słabe";
            strengthClass = "text-danger";
        } else if(strength < 35){
            strengthText = "słabe";
            strengthClass = "text-danger";
        } else if(strength < 59){
            strengthText = "wystarczające";
            strengthClass = "text-warning";
        } else if(strength < 127){
            strengthText = "silne";
            strengthClass = "text-success";
        } else{
            strengthText = "bardzo silne";
            strengthClass = "text-primary";
        }

        $('#password-strength').text(strengthText).removeClass().addClass(strengthClass);
    });

    $('#signin-submit').click((event) => {
        event.preventDefault();
        clearErrors();
        if(validateSignInForm())
            $('#signin-form').submit();

    });

    $('#signin-username-input').blur(() => {

        $.ajax({
            type: 'post',
            url: '/api/checkUsername',
            contentType: 'application/json',
            dataType: 'text',
            data: JSON.stringify({username: $('#signin-username-input').val()})
        }).done(resp => {
            if(resp === 'T') {
                $('#signin-username-error').text('Podany login jest już zajęty').attr('hidden', false);
                $('#signin-submit').attr('disabled', true);
            }
            else if(resp === 'F'){
                $('#signin-username-error').text('').attr('hidden', true);
                $('#signin-submit').attr('disabled', false);
            }

        });
    });

});



function validateSignInForm(){
    let username = $('#signin-username-input').val();
    let password = $('#signin-password-input').val();
    let repeatPassword = $('#signin-rep-password-input').val();
    let isValid = true;

    if(username.length < 5) {
        $('#signin-username-error').text('Nazwa użytkownika jest za krótka').attr('hidden', false);
        isValid = false;
    }
    if(!username.match(/^[a-z0-9]+$/i)) {
        $('#signin-username-error').text('Nazwa użytkownika może zawierać wyłącznie litery i cyfry').attr('hidden', false);
        isValid = false;
    }
    if(password.length < 8) {
        $('#signin-password-error').text('Hasło jest za krótkie').attr('hidden', false);
        isValid = false;
    }
    if(!password.match(/.*[A-Z].*/)){
        $('#signin-password-error').text('Hasło powinno zawierać minimum jedną wielką literę').attr('hidden', false);
        isValid = false;
    }
    if(!password.match(/.*[a-z].*/)){
        $('#signin-password-error').text('Hasło powinno zawierać minimum jedną małą literę').attr('hidden', false);
        isValid = false;
    }
    if(!password.match(/.*[0-9].*/)){
        $('#signin-password-error').text('Hasło powinno zawierać minimum jedną cyfrę').attr('hidden', false);
        isValid = false;
    }
    if(repeatPassword !== password) {
        $('#signin-rep-password-error').text('Hasła nie są takie same').attr('hidden', false);
        isValid = false;
    }
    return isValid;

}

function clearErrors(){
    $('#signin-username-error').text('').attr('hidden', true);
    $('#signin-password-error').text('').attr('hidden', true);
    $('#signin-rep-password-error').text('').attr('hidden', true);
}


function calculatePasswordStrength(){
    let password = $('#signin-password-input').val();

    if(!password)
        return 0;

    let pool = 0;
    if(password.match(/.*[0-9].*/))
        pool += 10;
    if(password.match(/.*[a-z].*/))
        pool += 26;
    if(password.match(/.*[A-Z].*/))
        pool += 26;
    if(password.match(/[`~!@#$%^&*()\-_=+\\|\[\]{};:'"<,>.? /]/))
        pool += 33;
    return password.length * Math.log2(pool)
}

