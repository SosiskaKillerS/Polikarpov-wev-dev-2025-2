document.addEventListener('DOMContentLoaded', function() {
    fetch('http://127.0.0.1:5000/check_session', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        if (!data.logged_in) {
            alert('Вы должны быть зарегистрированы');
            window.location.href = 'auth.html';
        } else {
            console.log('Добро пожаловать на секретную страницу!');
        }
    })
    .catch((error) => {
        console.error('Ошибка:', error);
    });
});