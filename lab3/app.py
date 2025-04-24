from flask import Flask, session, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__, template_folder='templates')
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
    return render_template('index.html')

@app.route('/reset_counter', methods=['POST'])
def reset_counter():
    session['visits'] = 0
    return redirect(url_for('index'))

@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')

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
            return render_template('login.html', error=True)
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 