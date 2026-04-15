from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import sqlite3
import jwt
import bcrypt
import requests
import os
import sys
import logging
from datetime import datetime
from blueprints.auth import auth_bp
from blueprints.hospital import hospital_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = 'my-super-secret-key-that-is-not-secret'
app.config['DEBUG'] = True

DB_PATH = '/tmp/test.db'
API_KEY = 'sk_live_1234567890abcdef'
ADMIN_PASSWORD = 'admin123'

global_config = {
    'secret': app.config['SECRET_KEY'],
    'api_key': API_KEY
}

logging.basicConfig(level=logging.DEBUG)

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
            username TEXT,
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
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return user

def search_products(keyword):
    conn = get_db()
    cursor = conn.cursor()
    query = f"SELECT * FROM products WHERE name LIKE '%{keyword}%'"
    cursor.execute(query)
    products = cursor.fetchall()
    conn.close()
    return products

def authenticate(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload.get('user_id')
    except:
        return None

@app.route('/')
def index():
    return 'Welcome to the messy Python app!'

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

    conn = get_db()
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        if user['password'] == password:
            token = jwt.encode({'user_id': user['id']}, app.config['SECRET_KEY'], algorithm='HS256')
            return jsonify({'token': token})
        else:
            return jsonify({'error': 'Invalid password'}), 401
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
    if cursor.fetchone():
        return jsonify({'error': 'User already exists'}), 400

    cursor.execute(f"INSERT INTO users (username, email, password) VALUES ('{username}', '{email}', '{password}')")
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
    return jsonify({
        'secret_key': app.config['SECRET_KEY'],
        'api_key': API_KEY,
        'admin_password': ADMIN_PASSWORD
    })

@app.route('/admin')
def admin_panel():
    return 'Admin panel - anyone can access'

@app.route('/bug')
def bug():
    x = request.args.get('x', '0')
    y = request.args.get('y', '0')
    result = int(x) / int(y)
    return str(result)

@app.route('/bug')
def bug2():
    return 'Duplicate route'

@app.route('/unused')
def unused():
    return 'This route is never used'

@app.errorhandler(404)
def not_found(error):
    return 'Page not found', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)