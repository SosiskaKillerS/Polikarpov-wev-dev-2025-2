document.addEventListener('DOMContentLoaded', function() {
    // Проверка активной сессии
    fetch('http://127.0.0.1:5000/check_session', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        if (data.logged_in) {
            window.location.href = 'secret_page.html';
        }
    })
    .catch((error) => {
        console.error('Ошибка:', error);
    });

    const form = document.getElementById('authForm');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const login = document.getElementById('login').value;
            const password = document.getElementById('password').value;
            const remember = document.getElementById('remember').checked;

            const data = {
                login: login,
                password: password,
                remember: remember
            };

            fetch('http://127.0.0.1:5000/submit', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data),
                credentials: 'include'
            })
            .then(response => response.json())
            .then(data => {
                if (data.message === 'Успешный вход') {
                    window.location.href = 'secret_page.html';
                } else {
                    alert('Неверный логин или пароль');
                }
            })
            .catch((error) => {
                console.error('Ошибка:', error);
            });
        });
    } else {
        console.error('Форма с id "authForm" не найдена');
    }
});