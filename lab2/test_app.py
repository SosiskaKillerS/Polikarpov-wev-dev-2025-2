import pytest
from app import app, validate_phone_number, format_phone_number

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Тесты для страницы URL параметров
def test_url_params_empty(client):
    response = client.get('/url-params')
    assert response.status_code == 200
    assert b'No URL parameters found' in response.data

def test_url_params_with_values(client):
    response = client.get('/url-params?name=John&age=25')
    assert response.status_code == 200
    assert b'name' in response.data
    assert b'John' in response.data
    assert b'age' in response.data
    assert b'25' in response.data

# Тесты для страницы заголовков
def test_headers_page(client):
    response = client.get('/headers')
    assert response.status_code == 200
    assert b'Request Headers' in response.data
    assert b'User-Agent' in response.data

# Тесты для работы с cookies
def test_set_cookie(client):
    response = client.post('/set_cookie', data={
        'cookie_name': 'test_cookie',
        'cookie_value': 'test_value'
    })
    assert response.status_code == 200
    assert 'test_cookie=test_value' in response.headers.get('Set-Cookie', '')

def test_delete_cookie(client):
    # Сначала устанавливаем cookie
    client.post('/set_cookie', data={
        'cookie_name': 'test_cookie',
        'cookie_value': 'test_value'
    })
    # Затем удаляем
    response = client.post('/delete_cookie', data={
        'cookie_name': 'test_cookie'
    })
    assert response.status_code == 200
    assert 'test_cookie=;' in response.headers.get('Set-Cookie', '')

# Тесты для валидации номера телефона
@pytest.mark.parametrize("phone,expected", [
    ("+7 (123) 456-75-90", (True, None)),
    ("8(123)4567590", (True, None)),
    ("123.456.75.90", (True, None)),
    ("123456789", (False, "Недопустимый ввод. Неверное количество цифр.")),
    ("123@456#7890", (False, "Недопустимый ввод. В номере телефона встречаются недопустимые символы."))
])
def test_phone_validation(phone, expected):
    result = validate_phone_number(phone)
    assert result == expected

# Тесты для форматирования номера телефона
@pytest.mark.parametrize("phone,expected", [
    ("+7 (123) 456-75-90", "8-123-456-75-90"),
    ("8(123)4567590", "8-123-456-75-90"),
    ("123.456.75.90", "8-123-456-75-90")
])
def test_phone_formatting(phone, expected):
    assert format_phone_number(phone) == expected

# Тесты для отображения на странице
def test_phone_validation_page_error_display(client):
    response = client.post('/validate_phone', data={
        'phone': '123@456#7890'
    })
    assert response.status_code == 200
    assert b'is-invalid' in response.data
    assert b'invalid-feedback' in response.data
    assert 'недопустимые символы'.encode('utf-8') in response.data

def test_phone_validation_page_success_display(client):
    response = client.post('/validate_phone', data={
        'phone': '123.456.75.90'
    })
    assert response.status_code == 200
    assert b'8-123-456-75-90' in response.data

def test_phone_validation_value_persistence(client):
    test_phone = '123@456#7890'
    response = client.post('/validate_phone', data={
        'phone': test_phone
    })
    assert response.status_code == 200
    assert test_phone.encode('utf-8') in response.data 