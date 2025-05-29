import pytest
from flask import session, url_for
from flask_login import current_user

# Импортируем приложение и необходимые классы из основного файла
from lab3.app import app, User, load_user


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Отключаем CSRF для тестов
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_index_page(client):
    """Тест доступности главной страницы"""
    response = client.get('/')
    assert response.status_code == 200
    assert 'Счётчик посещений'.encode('utf-8') in response.data


def test_session_counter(client):
    """Тест работы счетчика посещений в сессии"""
    client.get('/')
    assert session.get('visits') == 1

    client.get('/')
    assert session.get('visits') == 2

    client.post('/reset_counter')
    assert session.get('visits') == 0


def test_reset_counter_redirect(client):
    """Тест редиректа после сброса счетчика"""
    response = client.post('/reset_counter', follow_redirects=True)
    assert response.status_code == 200
    assert 'Счётчик посещений'.encode('utf-8') in response.data


def test_secret_page_unauthorized(client):
    """Тест доступа к секретной странице без авторизации"""
    response = client.get('/secret', follow_redirects=True)
    assert 'Вход в систему'.encode('utf-8') in response.data


def test_login_page(client):
    """Тест доступности страницы входа"""
    response = client.get('/login')
    assert response.status_code == 200
    assert 'Имя пользователя'.encode('utf-8') in response.data


def test_successful_login(client):
    """Тест успешной авторизации"""
    response = client.post('/login', data={
        'username': 'user',
        'password': 'qwerty',
        'remember': 'on'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert 'Счётчик посещений'.encode('utf-8') in response.data or 'Секретная страница'.encode('utf-8') in response.data


def test_failed_login(client):
    """Тест неудачной авторизации"""
    response = client.post('/login', data={
        'username': 'wrong',
        'password': 'wrong',
    }, follow_redirects=True)
    assert 'Неверное имя пользователя или пароль'.encode('utf-8') in response.data


def test_logout(client):
    """Тест выхода из системы"""
    # Сначала логинимся
    client.post('/login', data={
        'username': 'user',
        'password': 'qwerty'
    }, follow_redirects=True)

    # Затем выходим
    response = client.get('/logout', follow_redirects=True)
    assert 'Войти'.encode('utf-8') in response.data


def test_user_class():
    """Тест класса User"""
    user = User('test_id')
    assert user.get_id() == 'test_id'


def test_load_user():
    """Тест загрузки пользователя"""
    assert load_user('user') is not None
    assert load_user('invalid') is None


def test_navbar_for_anonymous(client):
    """Тест навбара для неавторизованного пользователя"""
    response = client.get('/')
    assert 'Секретная страница'.encode('utf-8') not in response.data
    assert 'Выйти'.encode('utf-8') not in response.data
    assert 'Войти'.encode('utf-8') in response.data


def test_navbar_for_authenticated(client):
    """Тест навбара для авторизованного пользователя"""
    client.post('/login', data={
        'username': 'user',
        'password': 'qwerty'
    }, follow_redirects=True)
    response = client.get('/')
    assert 'Секретная страница'.encode('utf-8') in response.data
    assert 'Выйти'.encode('utf-8') in response.data


def test_remember_me(client):
    """Тест функции 'запомнить меня'"""
    client.post('/login', data={
        'username': 'user',
        'password': 'qwerty',
        'remember': 'on'
    }, follow_redirects=True)
    # Проверяем, что сессия сохраняется
    assert '_user_id' in session


def test_redirect_after_login(client):
    """Тест редиректа после логина на запрошенную страницу"""
    response = client.get('/secret', follow_redirects=False)
    assert '/login' in response.location

    # Логинимся с параметром next
    response = client.post('/login?next=/secret', data={
        'username': 'user',
        'password': 'qwerty'
    }, follow_redirects=True)
    assert 'Секретная страница'.encode('utf-8') in response.data


def test_multiple_visits(client):
    """Тест нескольких посещений с сохранением сессии"""
    with client.session_transaction() as sess:
        sess['visits'] = 10

    response = client.get('/')
    assert session.get('visits') == 11


def test_logout_without_login(client):
    """Тест попытки выхода без входа"""
    response = client.get('/logout', follow_redirects=True)
    # Должен редиректить на логин
    assert 'Вход в систему'.encode('utf-8') in response.data


def test_double_login(client):
    """Тест двойного логина"""
    client.post('/login', data={
        'username': 'user',
        'password': 'qwerty'
    }, follow_redirects=True)
    response = client.post('/login', data={
        'username': 'user',
        'password': 'qwerty'
    }, follow_redirects=True)
    assert 'Счётчик посещений'.encode('utf-8') in response.data or 'Секретная страница'.encode('utf-8') in response.data


def test_welcome_message_for_authenticated(client):
    """Тест проверки сообщения приветствия для авторизованного пользователя"""
    client.post('/login', data={
        'username': 'user',
        'password': 'qwerty'
    }, follow_redirects=True)
    response = client.get('/')
    assert 'Добро пожаловать'.encode('utf-8') in response.data