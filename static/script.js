const form = document.getElementById('form');
const fieldset = document.getElementById('fieldset');
const submit = document.getElementById('submit');
const wait = document.getElementById('wait');
const notification = document.getElementById('notification');
const answer = document.getElementById('answer');
const code = document.getElementById('code');
const invalid_code = document.getElementById('invalid-code');
const date = document.getElementById('date');
const invalid_date = document.getElementById('invalid-date');
const hour = document.getElementById('hour');
const invalid_hour = document.getElementById('invalid-hour');

function validateCode(number) {
    var regex = /^[0-9]+$/;
    return regex.test(number);
}

function validateDate(date) {
    var regex = /^20([2-9]{1})([3-9]{1})-(0?[1-9]|1[0-2])-(0?[1-9]|1[0-9]|2[0-9]|3[0-1])$/;
    return regex.test(date);
}

function validateHour(hour) {
    var regex = /^([01]?[0-9]|2[0-3]):[0-5][0-9]$/;
    return regex.test(hour);
}

form.addEventListener('submit', (event) => {
    // Prevenir que el formulario se envíe automáticamente
    event.preventDefault();
    invalid_code.classList.add("is-hidden");
    invalid_date.classList.add("is-hidden");
    invalid_hour.classList.add("is-hidden");

    const is_valid_code = validateCode(code.value);
    const is_valid_date = validateDate(date.value);
    const is_valid_hour = validateHour(hour.value);

    if ( is_valid_code === false ) {
        invalid_code.classList.remove("is-hidden");
    }

    if ( is_valid_date === false ) {
        invalid_date.classList.remove("is-hidden");
    }

    if ( is_valid_hour === false ) {
        invalid_hour.classList.remove("is-hidden");
    }

    if (is_valid_code === false || is_valid_date === false  || is_valid_hour === false) {
        return;
    }

    // Obtener los datos del formulario
    var formData = new FormData(form);

    // Deshabilitar el formulario para evitar multiples requests
    fieldset.disabled = true;
    submit.classList.add('is-loading');
    notification.classList.add("is-hidden");
    wait.classList.remove("is-hidden");

    // Configurar la solicitud AJAX utilizando Fetch
    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(function(response) {
        fieldset.disabled = false;
        wait.classList.add("is-hidden");
        submit.classList.remove('is-loading');

        if (response.ok) {
            return response.text();
        } else {
            // La respuesta ha fallado, manejar el error
            throw new Error('La respuesta ha fallado.');
        }
    })
    .then(function(data) {
        const json = JSON.parse(data);
        // La respuesta ha sido exitosa, procesar la respuesta
        notification.classList.remove("is-hidden");
        answer.textContent = json.answer;
    })
    .catch(function(error) {
        console.error(error);
    });
});