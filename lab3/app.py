from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Create a user instance
user = User('user')

@login_manager.user_loader
def load_user(user_id):
    if user_id == 'user':
        return user
    return None

def get_navbar():
    return f'''
    <div class="navbar">
        <a href="/">Главная</a>
        <a href="/login">Войти</a>
        {f'<a href="/secret">Секретная страница</a>' if current_user.is_authenticated else ''}
        {f'<a href="/logout">Выйти</a>' if current_user.is_authenticated else ''}
    </div>
    '''

@app.route('/')
def index():
    if 'visits' not in session:
        session['visits'] = 0
    session['visits'] += 1
    
    return f'''
    <!DOCTYPE html>
    <html>
        <head>
            <title>Visit Counter</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f0f2f5;
                }}
                .navbar {{
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    background-color: #333;
                    padding: 1rem;
                    z-index: 1000;
                }}
                .navbar a {{
                    color: white;
                    text-decoration: none;
                    margin-right: 1rem;
                }}
                .content {{
                    margin-top: 80px;
                }}
                .counter {{
                    background-color: white;
                    padding: 2rem;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    text-align: center;
                    max-width: 600px;
                    margin: 0 auto;
                }}
                .number {{
                    font-size: 3rem;
                    color: #1a73e8;
                    margin: 1rem 0;
                }}
                .message {{
                    color: green;
                    margin: 1rem 0;
                }}
                .reset-button {{
                    background-color: #dc3545;
                    color: white;
                    border: none;
                    padding: 0.5rem 1rem;
                    border-radius: 4px;
                    cursor: pointer;
                    margin-top: 1rem;
                }}
                .reset-button:hover {{
                    background-color: #c82333;
                }}
            </style>
        </head>
        <body>
            {get_navbar()}
            <div class="content">
                <div class="counter">
                    <h1>Счётчик посещений</h1>
                    <div class="number">{session['visits']}</div>
                    <p>Вы посетили эту страницу</p>
                    {f'<p class="message">Добро пожаловать, {current_user.id}!</p>' if current_user.is_authenticated else ''}
                    <form action="/reset_counter" method="POST">
                        <button type="submit" class="reset-button">Обнулить счётчик</button>
                    </form>
                </div>
            </div>
        </body>
    </html>
    '''

@app.route('/reset_counter', methods=['POST'])
def reset_counter():
    session['visits'] = 0
    return redirect(url_for('index'))

@app.route('/secret')
@login_required
def secret():
    return f'''
    <!DOCTYPE html>
    <html>
        <head>
            <title>Секретная страница</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f0f2f5;
                }}
                .navbar {{
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    background-color: #333;
                    padding: 1rem;
                    z-index: 1000;
                }}
                .navbar a {{
                    color: white;
                    text-decoration: none;
                    margin-right: 1rem;
                }}
                .content {{
                    margin-top: 80px;
                }}
                .secret-content {{
                    background-color: white;
                    padding: 2rem;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    text-align: center;
                    max-width: 600px;
                    margin: 0 auto;
                }}
            </style>
        </head>
        <body>
            {get_navbar()}
            <div class="content">
                <div class="secret-content">
                    <h1>Секретная страница</h1>
                    <p>Поздравляем! Вы успешно вошли в систему.</p>
                    <p>Это секретная страница, доступная только авторизованным пользователям.</p>
                </div>
            </div>
        </body>
    </html>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        if username == 'user' and password == 'qwerty':
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('index'))
        else:
            return f'''
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Login</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 20px;
                            background-color: #f0f2f5;
                        }}
                        .navbar {{
                            position: fixed;
                            top: 0;
                            left: 0;
                            right: 0;
                            background-color: #333;
                            padding: 1rem;
                            z-index: 1000;
                        }}
                        .navbar a {{
                            color: white;
                            text-decoration: none;
                            margin-right: 1rem;
                        }}
                        .content {{
                            margin-top: 80px;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            min-height: calc(100vh - 80px);
                        }}
                        .login-form {{
                            background-color: white;
                            padding: 2rem;
                            border-radius: 10px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                            width: 300px;
                        }}
                        .form-group {{
                            margin-bottom: 1rem;
                        }}
                        label {{
                            display: block;
                            margin-bottom: 0.5rem;
                        }}
                        input[type="text"],
                        input[type="password"] {{
                            width: 100%;
                            padding: 0.5rem;
                            border: 1px solid #ddd;
                            border-radius: 4px;
                            box-sizing: border-box;
                        }}
                        button {{
                            width: 100%;
                            padding: 0.75rem;
                            background-color: #1a73e8;
                            color: white;
                            border: none;
                            border-radius: 4px;
                            cursor: pointer;
                        }}
                        button:hover {{
                            background-color: #1557b0;
                        }}
                        .error {{
                            color: red;
                            margin-bottom: 1rem;
                        }}
                    </style>
                </head>
                <body>
                    {get_navbar()}
                    <div class="content">
                        <div class="login-form">
                            <h2>Вход в систему</h2>
                            <p class="error">Неверный логин или пароль</p>
                            <form method="POST">
                                <div class="form-group">
                                    <label for="username">Логин:</label>
                                    <input type="text" id="username" name="username" required>
                                </div>
                                <div class="form-group">
                                    <label for="password">Пароль:</label>
                                    <input type="password" id="password" name="password" required>
                                </div>
                                <div class="form-group">
                                    <label>
                                        <input type="checkbox" name="remember"> Запомнить меня
                                    </label>
                                </div>
                                <button type="submit">Войти</button>
                            </form>
                        </div>
                    </div>
                </body>
            </html>
            '''
    
    return f'''
    <!DOCTYPE html>
    <html>
        <head>
            <title>Login</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f0f2f5;
                }}
                .navbar {{
                    position: fixed;
                    top: 0;
                    left: 0;
                    right: 0;
                    background-color: #333;
                    padding: 1rem;
                    z-index: 1000;
                }}
                .navbar a {{
                    color: white;
                    text-decoration: none;
                    margin-right: 1rem;
                }}
                .content {{
                    margin-top: 80px;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: calc(100vh - 80px);
                }}
                .login-form {{
                    background-color: white;
                    padding: 2rem;
                    border-radius: 10px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    width: 300px;
                }}
                .form-group {{
                    margin-bottom: 1rem;
                }}
                label {{
                    display: block;
                    margin-bottom: 0.5rem;
                }}
                input[type="text"],
                input[type="password"] {{
                    width: 100%;
                    padding: 0.5rem;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    box-sizing: border-box;
                }}
                button {{
                    width: 100%;
                    padding: 0.75rem;
                    background-color: #1a73e8;
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }}
                button:hover {{
                    background-color: #1557b0;
                }}
            </style>
        </head>
        <body>
            {get_navbar()}
            <div class="content">
                <div class="login-form">
                    <h2>Вход в систему</h2>
                    <form method="POST">
                        <div class="form-group">
                            <label for="username">Логин:</label>
                            <input type="text" id="username" name="username" required>
                        </div>
                        <div class="form-group">
                            <label for="password">Пароль:</label>
                            <input type="password" id="password" name="password" required>
                        </div>
                        <div class="form-group">
                            <label>
                                <input type="checkbox" name="remember"> Запомнить меня
                            </label>
                        </div>
                        <button type="submit">Войти</button>
                    </form>
                </div>
            </div>
        </body>
    </html>
    '''

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 