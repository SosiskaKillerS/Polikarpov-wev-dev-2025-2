from flask import Flask, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_session import Session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import timedelta

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_COOKIE_NAME'] = 'my_session_cookie'
app.config['SECRET_KEY'] = '123'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Время жизни сессии 1 день
CORS(app, supports_credentials=True)
Session(app)

login_manager = LoginManager()
login_manager.init_app(app)

users = {
    'user': {'password': 'qwerty'}
}

class User(UserMixin):
    def __init__(self, username):
        self.id = username

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')
    remember = data.get('remember')

    if login in users and users[login]['password'] == password:
        user = User(login)
        login_user(user, remember=remember)
        session['user_id'] = user.id  # Сохраняем user_id в сессии
        return jsonify({
            'login': login,
            'message': 'Успешный вход'
        }), 200
    else:
        return jsonify({
            'message': 'Неверный логин или пароль'
        }), 401

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Успешный выход'}), 200

@app.route('/counter_of_visits', methods=['GET'])
@login_required
def counter_of_visits():
    if 'visit_count' in session:
        session['visit_count'] = session.get('visit_count') + 1
    else:
        session['visit_count'] = 1
    print('Total visits: {}'.format(session.get('visit_count')))
    session.modified = True
    return jsonify({
        'visits': session['visit_count'],
                    }), 200

@app.route('/check_session', methods=['GET'])
def check_session():
    if current_user.is_authenticated:
        return jsonify({'logged_in': True}), 200
    else:
        return jsonify({'logged_in': False}), 200

@app.route('/secret_page', methods=['GET'])
@login_required
def secret_page():
    return jsonify({'message': 'Добро пожаловать на секретную страницу!'}), 200

if __name__ == '__main__':
    app.run(debug=True)