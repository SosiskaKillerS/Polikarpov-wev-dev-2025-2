from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime

app = Flask(__name__)

# PostgreSQL configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1231@localhost:5432/lab4web'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    second_name = db.Column(db.String(100), nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    hash_password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(30), nullable=False, default='user')
    date_of_creation = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)


@app.route('/')
def auth():
    return render_template('auth.html')

@app.route('/login', methods=['POST'])
def login():
    pass


if __name__ == '__main__':
    app.run(debug=True)