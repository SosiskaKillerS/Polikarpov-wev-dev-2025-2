from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import re

from werkzeug.utils import send_from_directory

app = Flask(__name__)
CORS(app, supports_credentials=True)


def validate_phone_number(phone_number: str):
    # Удаляем все пробелы, скобки и точки из номера, так как они допустимы
    cleaned_number = phone_number.replace(' ', '').replace('(', '').replace(')', '').replace('.', '')
    # Получаем только цифры
    numbers = ''.join(re.findall(r'\d', cleaned_number))
    
    # Проверяем на недопустимые символы (разрешаем только цифры, +, пробелы, скобки и точку)
    if re.search(r'[^0-9+\s().-]', phone_number):
        return {
            "status": "error",
            "message": "Invalid input. The phone number contains invalid characters."
        }
    elif (cleaned_number.startswith('+7') or cleaned_number.startswith('8')) and len(numbers) == 11:
        return {
            "status": "success",
            "message": "Correct form"
        }
    elif len(numbers) == 10:
        return {
            "status": "success",
            "message": "Correct form"
        }
    else:
        return {
            "status": "error",
            "message": "Invalid input. Incorrect number of digits."
        }


@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        phone_number = data.get('phone')

        # Получаем результат валидации
        validation_result = validate_phone_number(phone_number)

        # Определяем HTTP статус-код в зависимости от результата
        status_code = 400 if validation_result["status"] == "error" else 200

        return jsonify(validation_result), status_code

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route('/')
def index():
    return send_from_directory('static', 'Cookie.html')

@app.route('/check-cookie', methods=['GET'])
def check_cookie():
    cookie_value = request.cookies.get('myCookie')
    return jsonify({"cookieSet": bool(cookie_value)}), 200

@app.route('/toggle-cookie', methods=['POST'])
def toggle_cookie():
    response = make_response(jsonify({"cookieSet": False}))
    if request.cookies.get('myCookie'):
        response.set_cookie('myCookie', '', expires=0, path='/', httponly=True, samesite='Lax')  # Удаляем cookie
    else:
        response.set_cookie('myCookie', 'cookieValue', max_age=7 * 24 * 60 * 60, path='/', httponly=True, samesite='Lax')  # Устанавливаем cookie
        response.json = {"cookieSet": True}
    return response, 200

if __name__ == '__main__':
    app.run(debug=True)
