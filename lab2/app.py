from flask import Flask, render_template, request, redirect, url_for, make_response
import re

app = Flask(__name__, template_folder='templates') # шаблоны хранятся в templates

def validate_phone_number(phone):
    # Удаляем все разрешенные символы, кроме цифр
    digits = re.sub(r'[+\s\(\)\-\.]', '', phone)
    
    # Проверяем наличие недопустимых символов
    if not re.match(r'^[\d\s\(\)\-\.\+]+$', phone):
        return False, "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
    
    # Проверяем количество цифр
    if phone.startswith(('+7', '8')):
        if len(digits) != 11:
            return False, "Недопустимый ввод. Неверное количество цифр."
    else:
        if len(digits) != 10:
            return False, "Недопустимый ввод. Неверное количество цифр."
    
    return True, None

def format_phone_number(phone):
    # Удаляем все нецифровые символы
    digits = re.sub(r'\D', '', phone)
    
    # Форматируем номер в формат 8-***-***-**-**
    if len(digits) == 11:
        digits = digits[1:]  # Убираем первую цифру, если номер начинается с 8 или +7
    return f"8-{digits[:3]}-{digits[3:6]}-{digits[6:8]}-{digits[8:]}"

@app.route('/')
def index():
    return redirect(url_for('phone'))

@app.route('/phone')
def phone():
    return render_template('phone.html')

@app.route('/validate_phone', methods=['POST'])
def validate_phone():
    phone_number = request.form.get('phone', '')
    is_valid, error_message = validate_phone_number(phone_number)
    
    if not is_valid:
        return render_template('phone.html', 
                             error_message=error_message,
                             phone=phone_number)
    
    formatted_phone = format_phone_number(phone_number)
    return render_template('phone.html', 
                         formatted_phone=formatted_phone,
                         phone=phone_number)

@app.route('/cookies')
def cookies():
    return render_template('cookies.html')

@app.route('/set_cookie', methods=['POST'])
def set_cookie():
    cookie_name = request.form.get('cookie_name')
    cookie_value = request.form.get('cookie_value')
    
    if not cookie_name or not cookie_value:
        return render_template('cookies.html')
    
    if cookie_name in request.cookies:
        return render_template('cookies.html')
    
    response = make_response(render_template('cookies.html'))
    response.set_cookie(cookie_name, cookie_value)
    return response

@app.route('/delete_cookie', methods=['POST'])
def delete_cookie():
    cookie_name = request.form.get('cookie_name')
    
    if not cookie_name:
        return render_template('cookies.html')
    
    if cookie_name not in request.cookies:
        return render_template('cookies.html')
    
    response = make_response(render_template('cookies.html'))
    response.delete_cookie(cookie_name)
    return response

@app.route('/url-params')
def url_params():
    return render_template('url_params.html',
                         url=request.url,
                         args=request.args)

@app.route('/headers')
def headers():
    return render_template('headers.html',
                         headers=dict(request.headers))

if __name__ == '__main__':
    app.run(debug=True)