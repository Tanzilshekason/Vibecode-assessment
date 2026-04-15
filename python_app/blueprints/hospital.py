from flask import Blueprint, request, jsonify, g
import sqlite3
import os

hospital_bp = Blueprint('hospital', __name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(os.getenv('DB_PATH', '/tmp/test.db'))
        db.row_factory = sqlite3.Row
    return db

@hospital_bp.teardown_app_request
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Patients
@hospital_bp.route('/patients', methods=['GET'])
def get_patients():
    search = request.args.get('search', '')
    limit = request.args.get('limit', 100, type=int)
    
    db = get_db()
    cursor = db.cursor()
    
    query = "SELECT * FROM patients"
    params = []
    if search:
        query += " WHERE name LIKE ? OR phone LIKE ?"
        params.extend(['%' + search + '%', '%' + search + '%'])
    query += " LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    patients = []
    for row in rows:
        patients.append({
            'id': row['id'],
            'name': row['name'],
            'age': row['age'],
            'gender': row['gender'],
            'phone': row['phone'],
            'address': row['address'],
            'created_at': row['created_at']
        })
    
    return jsonify(patients)

@hospital_bp.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    row = cursor.fetchone()
    
    if not row:
        return jsonify({'error': 'Patient not found'}), 404
    
    patient = {
        'id': row['id'],
        'name': row['name'],
        'age': row['age'],
        'gender': row['gender'],
        'phone': row['phone'],
        'address': row['address']
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
    
    if not name or age is None or not gender or not phone or not address:
        return jsonify({'error': 'All fields required'}), 400
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO patients (name, age, gender, phone, address) VALUES (?, ?, ?, ?, ?)",
        (name, age, gender, phone, address)
    )
    db.commit()
    
    return jsonify({'message': 'Patient created successfully'}), 201

@hospital_bp.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    data = request.json
    
    allowed_fields = {'name', 'age', 'gender', 'phone', 'address'}
    updates = []
    params = []
    for field in allowed_fields:
        if field in data:
            updates.append(f"{field} = ?")
            params.append(data[field])
    
    if not updates:
        return jsonify({'error': 'No fields to update'}), 400
    
    params.append(patient_id)
    set_clause = ', '.join(updates)
    query = f"UPDATE patients SET {set_clause} WHERE id = ?"
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query, params)
    db.commit()
    
    return jsonify({'message': 'Patient updated successfully'})

@hospital_bp.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    db.commit()
    
    return jsonify({'message': 'Patient deleted successfully'})

# Doctors
@hospital_bp.route('/doctors', methods=['GET'])
def get_doctors():
    specialization = request.args.get('specialization', '')
    limit = request.args.get('limit', 50, type=int)
    
    db = get_db()
    cursor = db.cursor()
    
    query = "SELECT * FROM doctors"
    params = []
    if specialization:
        query += " WHERE specialization = ?"
        params.append(specialization)
    query += " LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    doctors = []
    for row in rows:
        doctors.append({
            'id': row['id'],
            'name': row['name'],
            'specialization': row['specialization'],
            'phone': row['phone'],
            'email': row['email'],
            'available': bool(row['available'])
        })
    
    return jsonify(doctors)

# Appointments
@hospital_bp.route('/appointments', methods=['GET'])
def get_appointments():
    patient_id = request.args.get('patient_id', type=int)
    doctor_id = request.args.get('doctor_id', type=int)
    
    db = get_db()
    cursor = db.cursor()
    
    query = "SELECT * FROM appointments"
    where_clauses = []
    params = []
    if patient_id:
        where_clauses.append("patient_id = ?")
        params.append(patient_id)
    if doctor_id:
        where_clauses.append("doctor_id = ?")
        params.append(doctor_id)
    
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    appointments = []
    for row in rows:
        appointments.append({
            'id': row['id'],
            'patient_id': row['patient_id'],
            'doctor_id': row['doctor_id'],
            'appointment_date': row['appointment_date'],
            'status': row['status'],
            'notes': row['notes'],
            'created_at': row['created_at']
        })
    
    return jsonify(appointments)

@hospital_bp.route('/appointments', methods=['POST'])
def create_appointment():
    data = request.json
    patient_id = data.get('patient_id')
    doctor_id = data.get('doctor_id')
    appointment_date = data.get('appointment_date')
    notes = data.get('notes', '')
    
    if not patient_id or not doctor_id or not appointment_date:
        return jsonify({'error': 'patient_id, doctor_id, and appointment_date required'}), 400
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO appointments (patient_id, doctor_id, appointment_date, notes) VALUES (?, ?, ?, ?)",
        (patient_id, doctor_id, appointment_date, notes)
    )
    db.commit()
    
    return jsonify({'message': 'Appointment created successfully'}), 201

@hospital_bp.route('/appointments/<int:appointment_id>/status', methods=['PUT'])
def update_appointment_status(appointment_id):
    data = request.json
    status = data.get('status')
    
    if not status:
        return jsonify({'error': 'status required'}), 400
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE appointments SET status = ? WHERE id = ?",
        (status, appointment_id)
    )
    db.commit()
    
    return jsonify({'message': 'Appointment status updated successfully'})

# Medical Records
@hospital_bp.route('/medical-records', methods=['GET'])
def get_medical_records():
    patient_id = request.args.get('patient_id', type=int)
    
    db = get_db()
    cursor = db.cursor()
    
    query = "SELECT * FROM medical_records"
    params = []
    if patient_id:
        query += " WHERE patient_id = ?"
        params.append(patient_id)
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    records = []
    for row in rows:
        records.append({
            'id': row['id'],
            'patient_id': row['patient_id'],
            'doctor_id': row['doctor_id'],
            'diagnosis': row['diagnosis'],
            'prescription': row['prescription'],
            'visit_date': row['visit_date']
        })
    
    return jsonify(records)

@hospital_bp.route('/medical-records', methods=['POST'])
def create_medical_record():
    data = request.json
    patient_id = data.get('patient_id')
    doctor_id = data.get('doctor_id')
    diagnosis = data.get('diagnosis')
    prescription = data.get('prescription')
    
    if not patient_id or not doctor_id or not diagnosis:
        return jsonify({'error': 'patient_id, doctor_id, and diagnosis required'}), 400
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO medical_records (patient_id, doctor_id, diagnosis, prescription) VALUES (?, ?, ?, ?)",
        (patient_id, doctor_id, diagnosis, prescription)
    )
    db.commit()
    
    return jsonify({'message': 'Medical record created successfully'}), 201

# Stats
@hospital_bp.route('/stats', methods=['GET'])
def get_hospital_stats():
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM patients")
    patient_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM doctors")
    doctor_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE status = 'scheduled'")
    scheduled_appointments = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM appointments WHERE status = 'completed'")
    completed_appointments = cursor.fetchone()[0]
    
    total = scheduled_appointments + completed_appointments
    completion_rate = (completed_appointments / total * 100) if total > 0 else 0
    
    return jsonify({
        'patient_count': patient_count,
        'doctor_count': doctor_count,
        'scheduled_appointments': scheduled_appointments,
        'completed_appointments': completed_appointments,
        'completion_rate': round(completion_rate, 2)
    })

# Search patients
@hospital_bp.route('/search/patients', methods=['GET'])
def search_patients():
    keyword = request.args.get('q', '')
    
    if not keyword:
        return jsonify({'error': 'Search query required'}), 400
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM patients WHERE name LIKE ? OR phone LIKE ? OR address LIKE ?",
        ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%')
    )
    rows = cursor.fetchall()
    
    patients = []
    for row in rows:
        patients.append({
            'id': row['id'],
            'name': row['name'],
            'age': row['age'],
            'gender': row['gender'],
            'phone': row['phone'],
            'address': row['address']
        })
    
    return jsonify(patients)