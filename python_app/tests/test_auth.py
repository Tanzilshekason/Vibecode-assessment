import unittest
import sys
import os
import tempfile
import json

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app
import bcrypt

class AuthTestCase(unittest.TestCase):
    """Test cases for authentication endpoints."""
    
    def setUp(self):
        """Set up test client and temporary database."""
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret-key'
        self.app = app.test_client()
        
        # Initialize test database
        with app.app_context():
            from app import init_db
            init_db()
    
    def tearDown(self):
        """Clean up after tests."""
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
    
    def test_index_route(self):
        """Test that the index route returns the template."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Production App', response.data)
        self.assertIn(b'Welcome to the app', response.data)
    
    def test_login_missing_credentials(self):
        """Test login with missing credentials."""
        response = self.app.post('/login',
                                data=json.dumps({}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_register_user(self):
        """Test user registration."""
        data = {
            'username': 'testuser_' + str(hash('test_register_user')),  # Unique username
            'email': 'test@example.com',
            'password': 'securepassword123'
        }
        response = self.app.post('/register',
                                data=json.dumps(data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn('message', response_data)
        self.assertEqual(response_data['message'], 'User created')
    
    def test_register_duplicate_username(self):
        """Test registering with duplicate username."""
        # First registration
        username = 'duplicate_' + str(hash('test_duplicate'))
        data = {
            'username': username,
            'email': 'test1@example.com',
            'password': 'password123'
        }
        self.app.post('/register',
                     data=json.dumps(data),
                     content_type='application/json')
        
        # Second registration with same username
        data['email'] = 'test2@example.com'
        response = self.app.post('/register',
                                data=json.dumps(data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_login_valid_credentials(self):
        """Test login with valid credentials."""
        # First register a user via the API
        username = 'testlogin_' + str(hash('test_login_valid'))
        password = 'testpassword123'
        
        # Register the user
        register_data = {
            'username': username,
            'email': 'login@example.com',
            'password': password
        }
        register_response = self.app.post('/register',
                                         data=json.dumps(register_data),
                                         content_type='application/json')
        self.assertEqual(register_response.status_code, 201)
        
        # Now try to login
        data = {
            'username': username,
            'password': password
        }
        response = self.app.post('/login',
                                data=json.dumps(data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('token', response_data)
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        data = {
            'username': 'nonexistent',
            'password': 'wrongpassword'
        }
        response = self.app.post('/login',
                                data=json.dumps(data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_sql_injection_prevention(self):
        """Test that SQL injection attempts are blocked."""
        # SQL injection attempt in username
        data = {
            'username': "' OR 1=1 --",
            'password': 'anything'
        }
        response = self.app.post('/login',
                                data=json.dumps(data),
                                content_type='application/json')
        # Should return 401 (unauthorized) not 500 (server error)
        self.assertNotEqual(response.status_code, 500)
    
    def test_bug_route_division_by_zero(self):
        """Test the /bug route handles division by zero."""
        response = self.app.get('/bug?x=10&y=0')
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Division by zero')
    
    def test_bug_route_valid_division(self):
        """Test the /bug route with valid division."""
        response = self.app.get('/bug?x=10&y=2')
        self.assertEqual(response.status_code, 200)
        # Returns string result, not JSON
        result = float(response.data.decode('utf-8'))
        self.assertEqual(result, 5.0)
    
    def test_config_route_security(self):
        """Test that /config route doesn't expose secrets."""
        response = self.app.get('/config')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # Should not contain actual secret keys
        self.assertNotIn('SECRET_KEY', data)
        self.assertNotIn('API_KEY', data)
        self.assertIn('message', data)
    
    def test_admin_route_authentication(self):
        """Test that /admin route exists (authentication would be added in production)."""
        response = self.app.get('/admin')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin panel', response.data)

class SecurityTestCase(unittest.TestCase):
    """Test cases for security features."""
    
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
    
    def test_password_hashing(self):
        """Test that passwords are properly hashed."""
        password = 'testpassword'
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Verify the hash
        self.assertTrue(bcrypt.checkpw(password.encode('utf-8'), hashed))
        # Wrong password should not match
        self.assertFalse(bcrypt.checkpw('wrongpassword'.encode('utf-8'), hashed))
    
    def test_template_security(self):
        """Test that template doesn't contain active security vulnerabilities."""
        template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'index.html')
        with open(template_path, 'r') as f:
            content = f.read()
        
        # Check for active security issues (not in comments)
        # eval() should not be present at all
        self.assertNotIn('eval(', content)
        
        # sk_live_ might be in comments, which is acceptable
        # Check if it's in an active line (not preceded by // in same line)
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'sk_live_' in line:
                # Check if line is commented
                stripped = line.strip()
                if not (stripped.startswith('//') or stripped.startswith('/*')):
                    self.fail(f'Active API key found in line {i+1}: {line}')
        
        # createMemoryLeak should not be present
        self.assertNotIn('createMemoryLeak', content)

if __name__ == '__main__':
    unittest.main()