from flask import Flask, request, jsonify, session, g, render_template
import sqlite3
import jwt
import bcrypt
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
from blueprints.auth import auth_bp
from blueprints.hospital import hospital_bp

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
app.config['DEBUG'] = os.getenv('DEBUG', 'False').lower() == 'true'

DB_PATH = os.getenv('DB_PATH', '/tmp/test.db')
API_KEY = os.getenv('API_KEY', '')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', '')

logging.basicConfig(level=logging.DEBUG if app.config['DEBUG'] else logging.WARNING)

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            email TEXT,
            password TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(hospital_bp, url_prefix='/hospital')

def get_user_by_id(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def search_products(keyword):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + keyword + '%',))
    products = cursor.fetchall()
    conn.close()
    return products

def authenticate(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload.get('user_id')
    except jwt.InvalidTokenError:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = get_user_by_id(user_id)
    if user:
        return jsonify(dict(user))
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        # Assume password is hashed with bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            token = jwt.encode({'user_id': user['id']}, app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({'token': token})
        else:
            return jsonify({'error': 'Invalid password'}), 401
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    # POST handling
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'All fields required'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return jsonify({'error': 'User already exists'}), 400

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                   (username, email, hashed))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User created'}), 201

@app.route('/products')
def list_products():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    conn.close()
    return jsonify([dict(p) for p in products])

@app.route('/search')
def search():
    keyword = request.args.get('q', '')
    products = search_products(keyword)
    return jsonify([dict(p) for p in products])

@app.route('/config')
def show_config():
    # Remove sensitive data exposure
    return jsonify({'message': 'Configuration hidden'})

@app.route('/admin')
def admin_panel():
    # Add authentication in real scenario
    return 'Admin panel - access restricted'

@app.route('/bug')
def bug():
    x = request.args.get('x', '0')
    y = request.args.get('y', '1')
    try:
        result = int(x) / int(y)
        return str(result)
    except ZeroDivisionError:
        return jsonify({'error': 'Division by zero'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid numbers'}), 400

@app.route('/unused')
def unused():
    return 'This route is never used'

@app.errorhandler(404)
def not_found(error):
    return 'Page not found', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])