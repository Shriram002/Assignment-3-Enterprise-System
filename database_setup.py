from flask import Flask, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///students.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    amount_due = db.Column(db.Float, nullable=False)


@app.before_request
def init_db():
    if not hasattr(app, 'db_initialized'):
        db.create_all()
        if Student.query.count() == 0:
            initial_students = [
                Student(first_name='Ajit', last_name='Shinde', dob=datetime.strptime('2000-01-01', '%Y-%m-%d'), amount_due=1000.0),
                Student(first_name='Sam', last_name='Curran', dob=datetime.strptime('1998-05-12', '%Y-%m-%d'), amount_due=1500.0),
                Student(first_name='Shriram', last_name='Yadav', dob=datetime.strptime('2001-09-23', '%Y-%m-%d'), amount_due=2000.0)
            ]
            db.session.bulk_save_objects(initial_students)
            db.session.commit()
        app.db_initialized = True
