import sqlite3
import os
from datetime import datetime

# Database connection (thread‑unsafe – only for scripts, not for web requests)
conn = sqlite3.connect(os.getenv('DB_PATH', '/tmp/test.db'), check_same_thread=False)
cursor = conn.cursor()

# Create tables (only once)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        email TEXT,
        password TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY,
        name TEXT,
        age INTEGER,
        gender TEXT,
        phone TEXT,
        address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY,
        name TEXT,
        specialization TEXT,
        phone TEXT,
        email TEXT,
        available BOOLEAN DEFAULT 1
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY,
        patient_id INTEGER,
        doctor_id INTEGER,
        appointment_date TIMESTAMP,
        status TEXT DEFAULT 'scheduled',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS medical_records (
        id INTEGER PRIMARY KEY,
        patient_id INTEGER,
        doctor_id INTEGER,
        diagnosis TEXT,
        prescription TEXT,
        visit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()

class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def save(self):
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
            (self.username, self.email, self.password)
        )
        conn.commit()

    @staticmethod
    def get_by_id(user_id):
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return User(row[1], row[2], row[3])
        return None

    @staticmethod
    def get_all():
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return [User(row[1], row[2], row[3]) for row in rows]

class Patient:
    def __init__(self, name, age, gender, phone, address):
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone
        self.address = address

    def save(self):
        cursor.execute(
            "INSERT INTO patients (name, age, gender, phone, address) VALUES (?, ?, ?, ?, ?)",
            (self.name, self.age, self.gender, self.phone, self.address)
        )
        conn.commit()

    @staticmethod
    def get_by_id(patient_id):
        cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        row = cursor.fetchone()
        if row:
            return Patient(row[1], row[2], row[3], row[4], row[5])
        return None

    @staticmethod
    def search_by_name(name):
        cursor.execute("SELECT * FROM patients WHERE name LIKE ?", ('%' + name + '%',))
        rows = cursor.fetchall()
        return [Patient(row[1], row[2], row[3], row[4], row[5]) for row in rows]

    def calculate_age_group(self):
        if self.age < 18:
            return 'child'
        elif self.age < 60:
            return 'adult'
        else:
            return 'senior'

class Doctor:
    def __init__(self, name, specialization, phone, email):
        self.name = name
        self.specialization = specialization
        self.phone = phone
        self.email = email

    def save(self):
        cursor.execute(
            "INSERT INTO doctors (name, specialization, phone, email) VALUES (?, ?, ?, ?)",
            (self.name, self.specialization, self.phone, self.email)
        )
        conn.commit()

    @staticmethod
    def get_by_id(doctor_id):
        cursor.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
        row = cursor.fetchone()
        if row:
            return Doctor(row[1], row[2], row[3], row[4])
        return None

    @staticmethod
    def get_by_specialization(specialization):
        cursor.execute("SELECT * FROM doctors WHERE specialization = ?", (specialization,))
        rows = cursor.fetchall()
        return [Doctor(row[1], row[2], row[3], row[4]) for row in rows]

class Appointment:
    def __init__(self, patient_id, doctor_id, appointment_date, notes=''):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.notes = notes

    def save(self):
        cursor.execute(
            "INSERT INTO appointments (patient_id, doctor_id, appointment_date, notes) VALUES (?, ?, ?, ?)",
            (self.patient_id, self.doctor_id, self.appointment_date, self.notes)
        )
        conn.commit()

    @staticmethod
    def get_by_id(appointment_id):
        cursor.execute("SELECT * FROM appointments WHERE id = ?", (appointment_id,))
        row = cursor.fetchone()
        if row:
            return Appointment(row[1], row[2], row[3], row[5])
        return None

    @staticmethod
    def get_by_patient(patient_id):
        cursor.execute("SELECT * FROM appointments WHERE patient_id = ?", (patient_id,))
        rows = cursor.fetchall()
        return [Appointment(row[1], row[2], row[3], row[5]) for row in rows]

    @staticmethod
    def get_by_doctor(doctor_id):
        cursor.execute("SELECT * FROM appointments WHERE doctor_id = ?", (doctor_id,))
        rows = cursor.fetchall()
        return [Appointment(row[1], row[2], row[3], row[5]) for row in rows]

class MedicalRecord:
    def __init__(self, patient_id, doctor_id, diagnosis, prescription):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.diagnosis = diagnosis
        self.prescription = prescription

    def save(self):
        cursor.execute(
            "INSERT INTO medical_records (patient_id, doctor_id, diagnosis, prescription) VALUES (?, ?, ?, ?)",
            (self.patient_id, self.doctor_id, self.diagnosis, self.prescription)
        )
        conn.commit()

    @staticmethod
    def get_by_patient(patient_id):
        cursor.execute("SELECT * FROM medical_records WHERE patient_id = ?", (patient_id,))
        rows = cursor.fetchall()
        return [MedicalRecord(row[1], row[2], row[3], row[4]) for row in rows]

    @staticmethod
    def search_by_diagnosis(diagnosis):
        cursor.execute("SELECT * FROM medical_records WHERE diagnosis LIKE ?", ('%' + diagnosis + '%',))
        rows = cursor.fetchall()
        return [MedicalRecord(row[1], row[2], row[3], row[4]) for row in rows]

# Helper functions
def get_patient_statistics():
    cursor.execute("SELECT COUNT(*) as total, AVG(age) as avg_age FROM patients")
    row = cursor.fetchone()
    return {'total_patients': row[0], 'average_age': row[1]}

def get_appointment_summary():
    cursor.execute("SELECT status, COUNT(*) as count FROM appointments GROUP BY status")
    rows = cursor.fetchall()
    return {row[0]: row[1] for row in rows}