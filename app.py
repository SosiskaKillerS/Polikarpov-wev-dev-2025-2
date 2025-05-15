from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask import Flask, render_template
try:
    from lab1_template.app.app import app as lab1_app
    from lab2.app import app as lab2_app
    from lab3.app import app as lab3_app
    from lab4.app import app as lab4_app
except ImportError as e:
    print(f'Ошибка импорта: {e}')
main_app = Flask(__name__)

@main_app.route('/')
def index():
    return render_template('index.html')

# Создаем основное приложение с DispatcherMiddleware
application = DispatcherMiddleware(main_app, {
    '/lab1': lab1_app,
    '/lab2': lab2_app,
    '/lab3': lab3_app,
    '/lab4': lab4_app
})

if __name__ == '__main__':
    run_simple('localhost', 5000, application, use_reloader=True) 