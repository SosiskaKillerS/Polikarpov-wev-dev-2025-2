document.addEventListener('DOMContentLoaded', function() {
    fetch('http://127.0.0.1:5000/counter_of_visits', {
        method: 'GET',
        credentials: 'include',  // Важно для отправки кук
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('visitCount').textContent = `Количество посещений: ${data.visits}`;
    })
    .catch(error => {
        console.error('Ошибка:', error);
        document.getElementById('visitCount').textContent = 'Ошибка загрузки данных';
    });
});