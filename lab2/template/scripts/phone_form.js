document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('phoneForm');
    const phoneInput = document.getElementById('phone');
    const feedbackDiv = phoneInput.nextElementSibling;

    function showError(message) {
        phoneInput.classList.add('is-invalid');
        phoneInput.classList.remove('is-valid');
        feedbackDiv.textContent = message;
        feedbackDiv.style.display = 'block';
        feedbackDiv.classList.add('invalid-feedback');
        feedbackDiv.classList.remove('valid-feedback');
    }

    function showSuccess(message) {
        phoneInput.classList.remove('is-invalid');
        phoneInput.classList.add('is-valid');
        feedbackDiv.textContent = message;
        feedbackDiv.style.display = 'block';
        feedbackDiv.classList.remove('invalid-feedback');
        feedbackDiv.classList.add('valid-feedback');
    }

    form.addEventListener('submit', async function(event) {
        event.preventDefault();
        const phoneNumber = phoneInput.value;

        try {
            const response = await fetch('http://localhost:5000/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ phone: phoneNumber })
            });

            const result = await response.json();

            console.log('📡 Статус ответа сервера:', response.status);
            console.log('📝 JSON-ответ сервера:', result);

            if (result.status === 'success') {
                console.log('✅ Сервер подтверждает корректность номера:', result.message);
                showSuccess(result.message);
            } else {
                console.error('❌ Ошибка валидации:', result.message);
                showError(result.message);
            }
        } catch (error) {
            console.error('❌ Ошибка запроса:', error);
            showError('Ошибка при отправке данных на сервер');
        }
    });

    // Очистка стилей валидации при начале ввода
    phoneInput.addEventListener('input', function() {
        phoneInput.classList.remove('is-invalid', 'is-valid');
        feedbackDiv.style.display = 'none';
        feedbackDiv.classList.remove('valid-feedback', 'invalid-feedback');
    });
});
