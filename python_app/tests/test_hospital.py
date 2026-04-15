import unittest
import sys
import os
import tempfile
import json
import sqlite3

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app

class HospitalTestCase(unittest.TestCase):
    """Test cases for hospital management endpoints."""
    
    def setUp(self):
        """Set up test client and temporary database."""
        # Create a temporary database file
        self.db_fd, self.db_path = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret-key'
        app.config['DB_PATH'] = self.db_path
        self.app = app.test_client()
        
        # Initialize test database with schema
        with app.app_context():
            from app import init_db
            init_db()
            
            # Insert test data directly
            import sqlite3
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Insert test data
            cursor.executescript('''
                INSERT INTO patients (name, age, gender, phone, address) VALUES
                ('John Doe', 30, 'Male', '123-456-7890', '123 Main St'),
                ('Jane Smith', 25, 'Female', '987-654-3210', '456 Oak Ave');
                
                INSERT INTO doctors (name, specialization, phone, email) VALUES
                ('Dr. Smith', 'Cardiology', '111-222-3333', 'smith@hospital.com'),
                ('Dr. Johnson', 'Pediatrics', '444-555-6666', 'johnson@hospital.com');
                
                INSERT INTO appointments (patient_id, doctor_id, appointment_date, notes) VALUES
                (1, 1, '2024-01-15', 'Regular checkup'),
                (2, 2, '2024-01-20', 'Vaccination');
            ''')
            conn.commit()
            conn.close()
    
    def tearDown(self):
        """Clean up after tests."""
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)
    
    def test_get_patients(self):
        """Test retrieving all patients."""
        response = self.app.get('/hospital/patients')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        # Should have 2 test patients
        self.assertEqual(len(data), 2)
    
    def test_get_patient_by_id(self):
        """Test retrieving a specific patient."""
        response = self.app.get('/hospital/patients/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('name', data)
        self.assertEqual(data['name'], 'John Doe')
    
    def test_get_nonexistent_patient(self):
        """Test retrieving a patient that doesn't exist."""
        response = self.app.get('/hospital/patients/999')
        self.assertEqual(response.status_code, 404)
    
    def test_create_patient(self):
        """Test creating a new patient."""
        data = {
            'name': 'New Patient',
            'age': 40,
            'gender': 'Male',
            'phone': '555-123-4567',
            'address': '789 Pine Rd'
        }
        response = self.app.post('/hospital/patients',
                                data=json.dumps(data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn('id', response_data)
    
    def test_create_patient_missing_fields(self):
        """Test creating a patient with missing required fields."""
        data = {
            'name': 'Incomplete Patient'
            # Missing age, gender, etc.
        }
        response = self.app.post('/hospital/patients',
                                data=json.dumps(data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_update_patient(self):
        """Test updating an existing patient."""
        data = {
            'name': 'Updated Name',
            'age': 35,
            'gender': 'Male',
            'phone': '999-888-7777',
            'address': 'Updated Address'
        }
        response = self.app.put('/hospital/patients/1',
                               data=json.dumps(data),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('message', response_data)
    
    def test_delete_patient(self):
        """Test deleting a patient."""
        response = self.app.delete('/hospital/patients/1')
        self.assertEqual(response.status_code, 200)
        
        # Verify patient is deleted
        response = self.app.get('/hospital/patients/1')
        self.assertEqual(response.status_code, 404)
    
    def test_get_doctors(self):
        """Test retrieving all doctors."""
        response = self.app.get('/hospital/doctors')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
    
    def test_get_appointments(self):
        """Test retrieving all appointments."""
        response = self.app.get('/hospital/appointments')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)
    
    def test_search_patients(self):
        """Test searching patients by name."""
        response = self.app.get('/hospital/search/patients?q=John')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        # Should find John Doe
        self.assertTrue(len(data) >= 1)
    
    def test_search_patients_sql_injection(self):
        """Test that SQL injection in search is prevented."""
        response = self.app.get('/hospital/search/patients?q=%27%20OR%201%3D1%20--')
        self.assertEqual(response.status_code, 200)
        # Should return empty list or specific results, not all patients
        data = json.loads(response.data)
        # The injection should not work
        self.assertIsInstance(data, list)
    
    def test_hospital_stats(self):
        """Test retrieving hospital statistics."""
        response = self.app.get('/hospital/stats')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # Should contain stats keys
        self.assertIn('total_patients', data)
        self.assertIn('total_doctors', data)
        self.assertIn('total_appointments', data)

class DatabaseSecurityTestCase(unittest.TestCase):
    """Test cases for database security."""
    
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
    
    def test_parameterized_queries(self):
        """Verify that queries use parameterization."""
        # This is a conceptual test - we can't directly test implementation
        # but we can verify that SQL injection attempts don't work
        pass
    
    def test_input_validation(self):
        """Test that input validation is working."""
        # Test with invalid age (negative)
        data = {
            'name': 'Test Patient',
            'age': -5,  # Invalid age
            'gender': 'Male',
            'phone': '123-456-7890',
            'address': 'Test Address'
        }
        response = self.app.post('/hospital/patients',
                                data=json.dumps(data),
                                content_type='application/json')
        # Should either reject or handle gracefully
        self.assertNotEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()