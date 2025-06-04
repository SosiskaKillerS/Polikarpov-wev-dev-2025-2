from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
import logging
from datetime import datetime
import hashlib
import re

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Необходим для flash сообщений

# PostgreSQL connection configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1231@localhost:5432/lab4web'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Отключаем отслеживание изменений для оптимизации

# Инициализируем SQLAlchemy с нашим приложением
db = SQLAlchemy(app)

# Создаем базовый класс для моделей
Base = declarative_base()

# Модель пользователя
class User(Base):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    second_name = db.Column(db.String(100))
    login = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    hash_password = db.Column(db.String(100), info={'generated': True})  # Указываем, что поле генерируется
    role = db.Column(db.String(50))
    date_of_creation = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(login='{self.login}', name='{self.name}')>"

    __mapper_args__ = {
        'exclude_properties': ['hash_password']  # Исключаем поле из INSERT запросов
    }

def hash_password(password):
    """Хеширование пароля с использованием SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_login(login):
    """Валидация логина"""
    if not login:
        return False, "Логин не может быть пустым"
    if len(login) < 5:
        return False, "Логин должен содержать не менее 5 символов"
    if not re.match(r'^[a-zA-Z0-9]+$', login):
        return False, "Логин должен содержать только латинские буквы и цифры"
    return True, ""

def validate_password(password):
    """Валидация пароля"""
    if not password:
        return False, "Пароль не может быть пустым"
    if len(password) < 8:
        return False, "Пароль должен содержать не менее 8 символов"
    if len(password) > 128:
        return False, "Пароль должен содержать не более 128 символов"
    if not re.search(r'[A-Z]', password):
        return False, "Пароль должен содержать хотя бы одну заглавную букву"
    if not re.search(r'[a-z]', password):
        return False, "Пароль должен содержать хотя бы одну строчную букву"
    if not re.search(r'[0-9]', password):
        return False, "Пароль должен содержать хотя бы одну цифру"
    if re.search(r'\s', password):
        return False, "Пароль не должен содержать пробелы"
    if not re.match(r'^[a-zA-Zа-яА-Я0-9~!?@#$%^&*_\-+()\[\]{}><\/\\|"\'\.,:;]+$', password):
        return False, "Пароль содержит недопустимые символы"
    return True, ""

def validate_name(name):
    """Валидация имени"""
    if not name:
        return False, "Имя не может быть пустым"
    return True, ""

def validate_middle_name(middle_name):
    """Валидация отчества"""
    if not middle_name:
        return False, "Отчество не может быть пустым"
    return True, ""

def validate_second_name(second_name):
    """Валидация фамилии"""
    if not second_name:
        return False, "Фамилия не может быть пустой"
    return True, ""

# тест подключения к базе данных
try:
    # Создаем движок базы данных
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    logger.info("Движок базы данных успешно создан")
    
    # Проверяем подключение
    with engine.connect() as connection:
        logger.info("Успешное подключение к базе данных!")
        
    # Создаем фабрику сессий для работы с БД
    Session = sessionmaker(bind=engine)
    logger.info("Фабрика сессий успешно создана")
    
    # Создаем все таблицы в базе данных
    Base.metadata.create_all(engine)
    logger.info("Таблицы успешно созданы")
    
except Exception as e:
    logger.error(f"Ошибка при подключении к базе данных: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        
        session = Session()
        try:
            user = session.query(User).filter_by(login=login, password=password).first()
            if user:
                flash('Успешная авторизация!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Неверный логин или пароль', 'error')
        except Exception as e:
            flash(f'Ошибка при авторизации: {str(e)}', 'error')
        finally:
            session.close()
            
    return render_template('login.html')

@app.route('/users')
def users():
    session = Session()
    try:
        users = session.query(User).all()
        return render_template('users.html', users=users)
    except Exception as e:
        flash(f'Ошибка при получении данных: {str(e)}', 'error')
        return redirect(url_for('index'))
    finally:
        session.close()

@app.route('/user/<int:user_id>')
def user_details(user_id):
    session = Session()
    try:
        user = session.query(User).get(user_id)
        if user:
            return render_template('user_details.html', user=user)
        else:
            flash('Пользователь не найден', 'error')
            return redirect(url_for('users'))
    except Exception as e:
        flash(f'Ошибка при получении данных: {str(e)}', 'error')
        return redirect(url_for('users'))
    finally:
        session.close()

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        session = Session()
        try:
            # Получаем данные из формы
            name = request.form.get('name')
            middle_name = request.form.get('middle_name')
            second_name = request.form.get('second_name')
            login = request.form.get('login')
            password = request.form.get('password')
            role = request.form.get('role') or None

            # Валидация данных
            errors = {}
            is_valid = True

            # Проверяем каждое поле
            name_valid, name_error = validate_name(name)
            if not name_valid:
                errors['name'] = name_error
                is_valid = False

            middle_name_valid, middle_name_error = validate_middle_name(middle_name)
            if not middle_name_valid:
                errors['middle_name'] = middle_name_error
                is_valid = False

            second_name_valid, second_name_error = validate_second_name(second_name)
            if not second_name_valid:
                errors['second_name'] = second_name_error
                is_valid = False

            login_valid, login_error = validate_login(login)
            if not login_valid:
                errors['login'] = login_error
                is_valid = False

            password_valid, password_error = validate_password(password)
            if not password_valid:
                errors['password'] = password_error
                is_valid = False

            if not is_valid:
                return render_template('add_user.html', errors=errors, form_data=request.form)

            # Проверяем, существует ли пользователь с таким логином
            existing_user = session.query(User).filter_by(login=login).first()
            if existing_user:
                flash('Пользователь с таким логином уже существует', 'error')
                return redirect(url_for('add_user'))

            # Создаем нового пользователя
            new_user = User(
                name=name,
                middle_name=middle_name,
                second_name=second_name,
                login=login,
                password=password,
                role=role,
                date_of_creation=datetime.utcnow()
            )

            # Добавляем пользователя в базу данных
            session.add(new_user)
            session.commit()

            flash('Пользователь успешно добавлен', 'success')
            return redirect(url_for('users'))

        except Exception as e:
            session.rollback()
            flash(f'Ошибка при добавлении пользователя: {str(e)}', 'error')
            return redirect(url_for('add_user'))
        finally:
            session.close()

    return render_template('add_user.html')

@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    session = Session()
    try:
        user = session.query(User).get(user_id)
        if not user:
            flash('Пользователь не найден', 'error')
            return redirect(url_for('users'))

        if request.method == 'POST':
            # Получаем данные из формы
            name = request.form.get('name')
            middle_name = request.form.get('middle_name')
            second_name = request.form.get('second_name')
            role = request.form.get('role') or None

            # Валидация данных
            errors = {}
            is_valid = True

            # Проверяем каждое поле
            name_valid, name_error = validate_name(name)
            if not name_valid:
                errors['name'] = name_error
                is_valid = False

            middle_name_valid, middle_name_error = validate_middle_name(middle_name)
            if not middle_name_valid:
                errors['middle_name'] = middle_name_error
                is_valid = False

            second_name_valid, second_name_error = validate_second_name(second_name)
            if not second_name_valid:
                errors['second_name'] = second_name_error
                is_valid = False

            if not is_valid:
                return render_template('edit_user.html', user=user, errors=errors)

            # Обновляем данные пользователя
            user.name = name
            user.middle_name = middle_name
            user.second_name = second_name
            user.role = role

            session.commit()
            flash('Пользователь успешно обновлен', 'success')
            return redirect(url_for('users'))

        return render_template('edit_user.html', user=user)

    except Exception as e:
        session.rollback()
        flash(f'Ошибка при обновлении пользователя: {str(e)}', 'error')
        return redirect(url_for('users'))
    finally:
        session.close()

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    session = Session()
    try:
        user = session.query(User).get(user_id)
        if not user:
            flash('Пользователь не найден', 'error')
            return redirect(url_for('users'))

        session.delete(user)
        session.commit()
        flash('Пользователь успешно удален', 'success')
    except Exception as e:
        session.rollback()
        flash(f'Ошибка при удалении пользователя: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('users'))

@app.route('/change_password/<int:user_id>', methods=['POST'])
def change_password(user_id):
    session = Session()
    try:
        user = session.query(User).get(user_id)
        if not user:
            flash('Пользователь не найден', 'error')
            return redirect(url_for('users'))

        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        # Проверяем текущий пароль
        if current_password != user.password:
            flash('Неверный текущий пароль', 'error')
            return redirect(url_for('users'))

        # Проверяем, что новый пароль и подтверждение совпадают
        if new_password != confirm_password:
            flash('Новый пароль и подтверждение не совпадают', 'error')
            return redirect(url_for('users'))

        # Валидируем новый пароль
        password_valid, password_error = validate_password(new_password)
        if not password_valid:
            flash(f'Ошибка валидации пароля: {password_error}', 'error')
            return redirect(url_for('users'))

        # Обновляем пароль
        user.password = new_password
        session.commit()
        flash('Пароль успешно изменен', 'success')

    except Exception as e:
        session.rollback()
        flash(f'Ошибка при изменении пароля: {str(e)}', 'error')
    finally:
        session.close()
    return redirect(url_for('users'))

if __name__ == '__main__':
    app.run(debug=True)