from flask import Flask, request, jsonify, send_from_directory
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

@app.route('/')
def index():
    return send_from_directory('', 'index.html')

# Create Operation
@app.route('/student', methods=['POST'])
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
    return jsonify({'message': 'Student added successfully!'}), 201

# Read Operation
@app.route('/student/<student_id>', methods=['GET'])
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
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.json
    student = Student.query.get(student_id)
    if student is None:
        return jsonify({'message': 'Student not found'}), 404
    student.first_name = data['first_name']
    student.last_name = data['last_name']
    student.dob = datetime.strptime(data['dob'], '%Y-%m-%d')
    student.amount_due = data['amount_due']
    db.session.commit()
    return jsonify({'message': 'Student updated successfully!'})

# Delete Operation
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if student is None:
        return jsonify({'message': 'Student not found'}), 404
    db.session.delete(student)
    db.session.commit()
    return jsonify({'message': 'Student deleted successfully!'})

# Show All Records

@app.route('/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([{
        'student_id': student.student_id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'dob': student.dob.strftime('%Y-%m-%d'),
        'amount_due': student.amount_due
    } for student in students])

@app.route('/config', methods=['GET'])
def get_config():
    # Attempt to get public IP from Render's metadata service
    try:
        metadata_url = 'http://169.254.169.254/latest/meta-data/public-ipv4'
        public_ip = requests.get(metadata_url).text
    except:
        public_ip = requests.get('https://api.ipify.org').text

    return jsonify({
        'api_url': f'http://{public_ip}:{os.getenv("PORT", 5000)}',
    })
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
