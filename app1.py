from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app1 = Flask(__name__)
app1.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app1)

class Student(db.Model):
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    amount_due = db.Column(db.Float, nullable=False)

@app1.route('/')
def index():
    return send_from_directory('', 'index.html')

# Create Operation
@app1.route('/student', methods=['POST'])
def add_student():
    data = request.get_json()
    new_student = Student(
        first_name=data['first_name'],
        last_name=data['last_name'],
        dob=datetime.strptime(data['dob'], '%Y-%m-%d'),
        amount_due=data['amount_due']
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify({'message': 'Student added successfully!'})

# Read Operation
@app1.route('/student/<student_id>', methods=['GET'])
def get_student(student_id):
    student = Student.query.get_or_404(student_id)
    return jsonify({
        'student_id': student.student_id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'dob': student.dob.strftime('%Y-%m-%d'),
        'amount_due': student.amount_due
    })

# Update Operation
@app1.route('/student/<student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    student = Student.query.get_or_404(student_id)

    student.first_name = data['first_name']
    student.last_name = data['last_name']
    student.dob = datetime.strptime(data['dob'], '%Y-%m-%d')
    student.amount_due = data['amount_due']

    db.session.commit()
    return jsonify({'message': 'Student updated successfully!'})

# Delete Operation
@app1.route('/student/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully!'})

# Show All Records
@app1.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    student_list = []
    for student in students:
        student_data = {
            'student_id': student.student_id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'dob': student.dob.strftime('%Y-%m-%d'),
            'amount_due': student.amount_due
        }
        student_list.append(student_data)
    return jsonify(student_list)

if __name__ == '__main__':
    app1.run(debug=True)
