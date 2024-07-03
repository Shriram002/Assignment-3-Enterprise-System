from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app1 = Flask(__name__)
app1.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app1)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    amount_due = db.Column(db.Float, nullable=False)

with app1.app_context():
    db.create_all()

    # Add initial data
    initial_students = [
        Student(first_name='Ajit', last_name='Shinde', dob=datetime.strptime('2000-01-01', '%Y-%m-%d'), amount_due=1000.0),
        Student(first_name='Sam', last_name='Curran', dob=datetime.strptime('1998-05-12', '%Y-%m-%d'), amount_due=1500.0),
        Student(first_name='Shriram', last_name='Yadav', dob=datetime.strptime('2001-09-23', '%Y-%m-%d'), amount_due=2000.0)
    ]

    # Add and commit the initial data0
    db.session.bulk_save_objects(initial_students)
    db.session.commit()