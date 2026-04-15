# HealthCare Pro - Hospital Management System

HealthCare Pro is a comprehensive hospital management system built with Flask. It streamlines hospital operations including patient management, doctor scheduling, appointment booking, and medical record keeping.

## Features

- **Patient Management**: Register and manage patient information, medical history
- **Doctor Management**: Maintain doctor profiles, specializations, and availability
- **Appointment Scheduling**: Book, reschedule, and track patient appointments
- **Medical Records**: Digital medical records with diagnosis and prescriptions
- **Reporting**: Generate hospital statistics and patient reports
- **Search Functionality**: Search patients, doctors, and medical records

## Tech Stack

- Python 3.7+
- Flask 1.0.2
- SQLite database
- SQLAlchemy (planned)
- Jinja2 templating
- RESTful API

## Getting Started

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. Clone the repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Initialize the database:
   ```bash
   python app.py
   # The app will create necessary tables on first run
   ```
5. Start the server:
   ```bash
   python app.py
   ```
6. Visit `http://localhost:5000`

## Project Structure

- `app.py` - Main Flask application entry point
- `models.py` - Data models for User, Patient, Doctor, Appointment, MedicalRecord
- `blueprints/` - Modular route blueprints
  - `auth.py` - Authentication routes (login, register, profile)
  - `hospital.py` - Hospital management routes (patients, doctors, appointments)
- `config/` - Configuration files
- `utils/` - Utility functions and database helpers
- `static/` - Static assets (CSS, JavaScript, images)
- `templates/` - HTML templates (Jinja2)
- `tests/` - Test files

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /auth/profile` - Get user profile

### Patient Management
- `GET /hospital/patients` - List all patients
- `POST /hospital/patients` - Create a new patient
- `GET /hospital/patients/<id>` - Get patient details
- `PUT /hospital/patients/<id>` - Update patient information
- `DELETE /hospital/patients/<id>` - Delete patient

### Doctor Management
- `GET /hospital/doctors` - List all doctors
- `GET /hospital/doctors?specialization=<spec>` - Filter doctors by specialization

### Appointments
- `GET /hospital/appointments` - List appointments
- `POST /hospital/appointments` - Create a new appointment
- `PUT /hospital/appointments/<id>/status` - Update appointment status

### Medical Records
- `GET /hospital/medical-records` - List medical records
- `POST /hospital/medical-records` - Create a new medical record
- `GET /hospital/medical-records?patient_id=<id>` - Get patient's medical history

### Statistics
- `GET /hospital/stats` - Get hospital statistics

## Development Notes

This repository is intentionally messy and contains a production-like project with various issues including security vulnerabilities, poor structure, duplicate logic, missing validation, no tests, and bugs in logic. The codebase serves as an exercise for developers to identify and fix these problems.

## License

MIT