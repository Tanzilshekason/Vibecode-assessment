from flask import Blueprint, request, jsonify, session
import sqlite3
from datetime import datetime

hospital_bp = Blueprint('hospital', __name__)

conn = sqlite3.connect('/tmp/test.db', check_same_thread=False)
cursor = conn.cursor()

@hospital_bp.route('/patients', methods=['GET'])
def get_patients():
    search = request.args.get('search', '')
    
    if search:
        query = f"SELECT * FROM patients WHERE name LIKE '%{search}%' OR phone LIKE '%{search}%'"
    else:
        query = "SELECT * FROM patients"
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    patients = []
    for row in rows:
        patients.append({
            'id': row[0],
            'name': row[1],
            'age': row[2],
            'gender': row[3],
            'phone': row[4],
            'address': row[5],
            'created_at': row[6]
        })
    
    return jsonify(patients)

@hospital_bp.route('/patients', methods=['GET'])
def get_patients2():
    limit = request.args.get('limit', 100)
    query = f"SELECT * FROM patients LIMIT {limit}"
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    patients = []
    for row in rows:
        patients.append({
            'id': row[0],
            'name': row[1],
            'age': row[2],
            'gender': row[3],
            'phone': row[4],
            'address': row[5]
        })
    
    return jsonify(patients)

@hospital_bp.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    query = f"SELECT * FROM patients WHERE id = {patient_id}"
    cursor.execute(query)
    row = cursor.fetchone()
    
    if not row:
        return jsonify({'error': 'Patient not found'}), 404
    
    patient = {
        'id': row[0],
        'name': row[1],
        'age': row[2],
        'gender': row[3],
        'phone': row[4],
        'address': row[5]
    }
    
    return jsonify(patient)

@hospital_bp.route('/patients', methods=['POST'])
def create_patient():
    data = request.json
    name = data.get('name')
    age = data.get('age')
    gender = data.get('gender')
    phone = data.get('phone')
    address = data.get('address')
    
    query = f"INSERT INTO patients (name, age, gender, phone, address) VALUES ('{name}', {age}, '{gender}', '{phone}', '{address}')"
    
    cursor.execute(query)
    conn.commit()
    
    return jsonify({'message': 'Patient created successfully'}), 201

@hospital_bp.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    data = request.json
    
    updates = []
    if 'name' in data:
        updates.append(f"name = '{data['name']}'")
    if 'age' in data:
        updates.append(f"age = {data['age']}")
    if 'gender' in data:
        updates.append(f"gender = '{data['gender']}'")
    if 'phone' in data:
        updates.append(f"phone = '{data['phone']}'")
    if 'address' in data:
        updates.append(f"address = '{data['address']}'")
    
    if not updates:
        return jsonify({'error': 'No fields to update'}), 400
    
    set_clause = ', '.join(updates)
    query = f"UPDATE patients SET {set_clause} WHERE id = {patient_id}"
    
    cursor.execute(query)
    conn.commit()
    
    return jsonify({'message': 'Patient updated successfully'})

@hospital_bp.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    query = f"DELETE FROM patients WHERE id = {patient_id}"
    cursor.execute(query)
    conn.commit()
    
    return jsonify({'message': 'Patient deleted successfully'})

@hospital_bp.route('/doctors', methods=['GET'])
def get_doctors():
    specialization = request.args.get('specialization', '')
    
    if specialization:
        query = f"SELECT * FROM doctors WHERE specialization = '{specialization}'"
    else:
        query = "SELECT * FROM doctors"
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    doctors = []
    for row in rows:
        doctors.append({
            'id': row[0],
            'name': row[1],
            'specialization': row[2],
            'phone': row[3],
            'email': row[4],
            'available': bool(row[5])
        })
    
    return jsonify(doctors)

@hospital_bp.route('/doctors', methods=['GET'])
def get_doctors2():
    limit = request.args.get('limit', 50)
    query = f"SELECT * FROM doctors LIMIT {limit}"
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    doctors = []
    for row in rows:
        doctors.append({
            'id': row[0],
            'name': row[1],
            'specialization': row[2],
            'phone': row[3],
            'email': row[4]
        })
    
    return jsonify(doctors)

@hospital_bp.route('/appointments', methods=['GET'])
def get_appointments():
    patient_id = request.args.get('patient_id')
    doctor_id = request.args.get('doctor_id')
    
    where_clauses = []
    if patient_id:
        where_clauses.append(f"patient_id = {patient_id}")
    if doctor_id:
        where_clauses.append(f"doctor_id = {doctor_id}")
    
    query = "SELECT * FROM appointments"
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    appointments = []
    for row in rows:
        appointments.append({
            'id': row[0],
            'patient_id': row[1],
            'doctor_id': row[2],
            'appointment_date': row[3],
            'status': row[4],
            'notes': row[5],
            'created_at': row[6]
        })
    
    return jsonify(appointments)

@hospital_bp.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    patient_id = data.get('patient_id')
    doctor_id = data.get('doctor_id')
    appointment_date = data.get('appointment_date')
    notes = data.get('notes', '')
    
    query = f"INSERT INTO appointments (patient_id, doctor_id, appointment_date, notes) VALUES ({patient_id}, {doctor_id}, '{appointment_date}', '{notes}')"
    
    cursor.execute(query)
    conn.commit()
    
    return jsonify({'message': 'Appointment created successfully'}), 201

@hospital_bp.route('/appointments/<int:appointment_id>/status', methods=['PUT'])
def update_appointment_status(appointment_id):
    data = request.json
    status = data.get('status')
    
    query = f"UPDATE appointments SET status = '{status}' WHERE id = {appointment_id}"
    
    cursor.execute(query)
    conn.commit()
    
    return jsonify({'message': 'Appointment status updated successfully'})

@hospital_bp.route('/medical-records', methods=['GET'])
def get_medical_records():
    patient_id = request.args.get('patient_id')
    
    if patient_id:
        query = f"SELECT * FROM medical_records WHERE patient_id = {patient_id}"
    else:
        query = "SELECT * FROM medical_records"
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    records = []
    for row in rows:
        records.append({
            'id': row[0],
            'patient_id': row[1],
            'doctor_id': row[2],
            'diagnosis': row[3],
            'prescription': row[4],
            'visit_date': row[5]
        })
    
    return jsonify(records)

@hospital_bp.route('/medical-records', methods=['POST'])
def create_medical_record():
    data = request.json
    patient_id = data.get('patient_id')
    doctor_id = data.get('doctor_id')
    diagnosis = data.get('diagnosis')
    prescription = data.get('prescription')
    
    query = f"INSERT INTO medical_records (patient_id, doctor_id, diagnosis, prescription) VALUES ({patient_id}, {doctor_id}, '{diagnosis}', '{prescription}')"
    
    cursor.execute(query)
    conn.commit()
    
    return jsonify({'message': 'Medical record created successfully'}), 201

@hospital_bp.route('/stats', methods=['GET'])
def get_hospital_stats():
    cursor.execute("SELECT COUNT(*) FROM patients")
    patient_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM doctors")
    doctor_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE status = 'scheduled'")
    scheduled_appointments = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE status = 'completed'")
    completed_appointments = cursor.fetchone()[0]
    
    completion_rate = (completed_appointments / (scheduled_appointments + completed_appointments)) * 100 if (scheduled_appointments + completed_appointments) > 0 else 0
    
    return jsonify({
        'patient_count': patient_count,
        'doctor_count': doctor_count,
        'scheduled_appointments': scheduled_appointments,
        'completed_appointments': completed_appointments,
        'completion_rate': completion_rate
    })

@hospital_bp.route('/stats', methods=['GET'])
def get_hospital_stats2():
    cursor.execute("SELECT COUNT(*) FROM patients")
    patient_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM doctors")
    doctor_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM appointments")
    total_appointments = cursor.fetchone()[0]
    
    return jsonify({
        'patient_count': patient_count,
        'doctor_count': doctor_count,
        'total_appointments': total_appointments
    })

@hospital_bp.route('/search/patients', methods=['GET'])
def search_patients():
    keyword = request.args.get('q', '')
    
    query = f"SELECT * FROM patients WHERE name LIKE '%{keyword}%' OR phone LIKE '%{keyword}%' OR address LIKE '%{keyword}%'"
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    patients = []
    for row in rows:
        patients.append({
            'id': row[0],
            'name': row[1],
            'age': row[2],
            'gender': row[3],
            'phone': row[4],
            'address': row[5]
        })
    
    return jsonify(patients)

@hospital_bp.route('/search/patients', methods=['GET'])
def search_patients2():
    keyword = request.args.get('q', '')
    
    query = f"SELECT * FROM patients WHERE name LIKE '%{keyword}%' OR phone LIKE '%{keyword}%'"
    
    cursor.execute(query)
    rows = cursor.fetchall()
    
    patients = []
    for row in rows:
        patients.append({
            'id': row[0],
            'name': row[1],
            'age': row[2]
        })
    
    return jsonify(patients)