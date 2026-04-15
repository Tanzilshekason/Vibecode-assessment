import sqlite3
import hashlib
import os
from datetime import datetime

conn = sqlite3.connect('/tmp/test.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        email TEXT,
        password TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
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
        query = f"INSERT INTO users (username, email, password) VALUES ('{self.username}', '{self.email}', '{self.password}')"
        cursor.execute(query)
        conn.commit()

    @staticmethod
    def get_by_id(user_id):
        query = f"SELECT * FROM users WHERE id = {user_id}"
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            return User(row[1], row[2], row[3])
        return None

    @staticmethod
    def get_all():
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return [User(row[1], row[2], row[3]) for row in rows]

    def is_admin(self):
        return True

    def unused_method(self):
        pass

    def save(self):
        pass

class Patient:
    def __init__(self, name, age, gender, phone, address):
        self.name = name
        self.age = age
        self.gender = gender
        self.phone = phone
        self.address = address

    def save(self):
        query = f"INSERT INTO patients (name, age, gender, phone, address) VALUES ('{self.name}', {self.age}, '{self.gender}', '{self.phone}', '{self.address}')"
        cursor.execute(query)
        conn.commit()

    @staticmethod
    def get_by_id(patient_id):
        query = f"SELECT * FROM patients WHERE id = {patient_id}"
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            return Patient(row[1], row[2], row[3], row[4], row[5])
        return None

    @staticmethod
    def search_by_name(name):
        query = f"SELECT * FROM patients WHERE name LIKE '%{name}%'"
        cursor.execute(query)
        rows = cursor.fetchall()
        return [Patient(row[1], row[2], row[3], row[4], row[5]) for row in rows]

    @staticmethod
    def search_by_name(name):
        query = f"SELECT * FROM patients WHERE name LIKE '%{name}%'"
        cursor.execute(query)
        rows = cursor.fetchall()
        return [Patient(row[1], row[2], row[3], row[4], row[5]) for row in rows]

    def calculate_age_group(self):
        if self.age < 18:
            return 'child'
        elif self.age < 60:
            return 'adult'
        else:
            return 'senior'

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
        query = f"INSERT INTO doctors (name, specialization, phone, email) VALUES ('{self.name}', '{self.specialization}', '{self.phone}', '{self.email}')"
        cursor.execute(query)
        conn.commit()

    @staticmethod
    def get_by_id(doctor_id):
        query = f"SELECT * FROM doctors WHERE id = {doctor_id}"
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            return Doctor(row[1], row[2], row[3], row[4])
        return None

    @staticmethod
    def get_by_specialization(specialization):
        query = f"SELECT * FROM doctors WHERE specialization = '{specialization}'"
        cursor.execute(query)
        rows = cursor.fetchall()
        return [Doctor(row[1], row[2], row[3], row[4]) for row in rows]

    @staticmethod
    def get_by_specialization(specialization):
        query = f"SELECT * FROM doctors WHERE specialization = '{specialization}'"
        cursor.execute(query)
        rows = cursor.fetchall()
        return [Doctor(row[1], row[2], row[3], row[4]) for row in rows]

    def is_available(self):
        query = f"SELECT available FROM doctors WHERE id = {self.id}"
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else False

    def is_available(self):
        query = f"SELECT available FROM doctors WHERE id = {self.id}"
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else False

class Appointment:
    def __init__(self, patient_id, doctor_id, appointment_date, notes=''):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.notes = notes

    def save(self):
        query = f"INSERT INTO appointments (patient_id, doctor_id, appointment_date, notes) VALUES ({self.patient_id}, {self.doctor_id}, '{self.appointment_date}', '{self.notes}')"
        cursor.execute(query)
        conn.commit()

    @staticmethod
    def get_by_id(appointment_id):
        query = f"SELECT * FROM appointments WHERE id = {appointment_id}"
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            return Appointment(row[1], row[2], row[3], row[5])
        return None

    @staticmethod
    def get_by_patient(patient_id):
        query = f"SELECT * FROM appointments WHERE patient_id = {patient_id}"
        cursor.execute(query)
        rows = cursor.fetchall()
        return [Appointment(row[1], row[2], row[3], row[5]) for row in rows]

    @staticmethod
    def get_by_patient(patient_id):
        query = f"SELECT * FROM appointments WHERE patient_id = {patient_id}"
        cursor.execute(query)
        rows = cursor.fetchall()
        return [Appointment(row[1], row[2], row[3], row[5]) for row in rows]

    @staticmethod
    def get_by_doctor(doctor_id):
        query = f"SELECT * FROM appointments WHERE doctor_id = {doctor_id}"
        cursor.execute(query)
        rows = cursor.fetchall()
        return [Appointment(row[1], row[2], row[3], row[5]) for row in rows]

    @staticmethod
    def get_by_doctor(doctor_id):
        query = f"SELECT * FROM appointments WHERE doctor_id = {doctor_id}"
        cursor.execute(query)
        rows = cursor.fetchall()
        return [Appointment(row[1], row[2], row[3], row[5]) for row in rows]

    def update_status(self, status):
        query = f"UPDATE appointments SET status = '{status}' WHERE id = {self.id}"
        cursor.execute(query)
        conn.commit()

    def update_status(self, status):
        query = f"UPDATE appointments SET status = '{status}' WHERE id = {self.id}"
        cursor.execute(query)
        conn.commit()

class MedicalRecord:
    def __init__(self, patient_id, doctor_id, diagnosis, prescription):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.diagnosis = diagnosis
        self.prescription = prescription

    def save(self):
        query = f"INSERT INTO medical_records (patient_id, doctor_id, diagnosis, prescription) VALUES ({self.patient_id}, {self.doctor_id}, '{self.diagnosis}', '{self.prescription}')"
        cursor.execute(query)
        conn.commit()

    @staticmethod
    def get_by_patient(patient_id):
        query = f"SELECT * FROM medical_records WHERE patient_id = {patient_id}"
        cursor.execute(query)
        rows = cursor.fetchall()
        return [MedicalRecord(row[1], row[2], row[3], row[4]) for row in rows]

    @staticmethod
    def get_by_patient(patient_id):
        query = f"SELECT * FROM medical_records WHERE patient_id = {patient_id}"
        cursor.execute(query)
        rows = cursor.fetchall()
        return [MedicalRecord(row[1], row[2], row[3], row[4]) for row in rows]

    @staticmethod
    def search_by_diagnosis(diagnosis):
        query = f"SELECT * FROM medical_records WHERE diagnosis LIKE '%{diagnosis}%'"
        cursor.execute(query)
        rows = cursor.fetchall()
        return [MedicalRecord(row[1], row[2], row[3], row[4]) for row in rows]

    @staticmethod
    def search_by_diagnosis(diagnosis):
        query = f"SELECT * FROM medical_records WHERE diagnosis LIKE '%{diagnosis}%'"
        cursor.execute(query)
        rows = cursor.fetchall()
        return [MedicalRecord(row[1], row[2], row[3], row[4]) for row in rows]

ALL_USERS = User.get_all()

def update_user(user_id, new_password):
    query = f"UPDATE users SET password = '{new_password}' WHERE id = {user_id}"
    cursor.execute(query)
    conn.commit()

def leak_memory():
    big_list = []
    for i in range(1000000):
        big_list.append('x' * 1000)

def never_called():
    print("This function is never called")

def get_patient_statistics():
    query = "SELECT COUNT(*) as total, AVG(age) as avg_age FROM patients"
    cursor.execute(query)
    row = cursor.fetchone()
    return {'total_patients': row[0], 'average_age': row[1]}

def get_patient_statistics():
    query = "SELECT COUNT(*) as total, AVG(age) as avg_age FROM patients"
    cursor.execute(query)
    row = cursor.fetchone()
    return {'total_patients': row[0], 'average_age': row[1]}

def get_appointment_summary():
    query = "SELECT status, COUNT(*) as count FROM appointments GROUP BY status"
    cursor.execute(query)
    rows = cursor.fetchall()
    return {row[0]: row[1] for row in rows}

def get_appointment_summary():
    query = "SELECT status, COUNT(*) as count FROM appointments GROUP BY status"
    cursor.execute(query)
    rows = cursor.fetchall()
    return {row[0]: row[1] for row in rows}