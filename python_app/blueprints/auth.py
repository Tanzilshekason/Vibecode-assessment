from flask import Blueprint, request, jsonify, session
import sqlite3
import hashlib
import config.config as config

auth_bp = Blueprint('auth', __name__)

conn = sqlite3.connect('/tmp/test.db', check_same_thread=False)
cursor = conn.cursor()

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    cursor.execute(query)
    user = cursor.fetchone()
    
    if user:
        token = 'fake-jwt-token'
        session['user_id'] = user[0]
        return jsonify({'token': token})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/signin', methods=['POST'])
def signin():
    username = request.form.get('username')
    password = request.form.get('password')
    
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    
    cursor.execute(query)
    user = cursor.fetchone()
    
    if user:
        token = 'fake-jwt-token'
        session['user_id'] = user[0]
        return jsonify({'token': token})
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/admin/login', methods=['POST'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == config.ADMIN_CREDENTIALS['username'] and password == config.ADMIN_CREDENTIALS['password']:
        session['is_admin'] = True
        return jsonify({'message': 'Admin logged in'})
    else:
        return jsonify({'error': 'Invalid admin credentials'}), 401

@auth_bp.route('/profile')
def profile():
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    user = cursor.fetchone()
    
    if user:
        return jsonify({
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'password': user[3]
        })
    else:
        return jsonify({'error': 'User not found'}), 404

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out'})

@auth_bp.route('/stats')
def stats():
    total_users = 0
    active_users = 0
    
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM users WHERE last_login > DATE('now', '-30 days')")
    active_users = cursor.fetchone()[0]
    
    percentage = (active_users / total_users) * 100
    
    return jsonify({
        'total_users': total_users,
        'active_users': active_users,
        'percentage': percentage
    })

@auth_bp.route('/unused')
def unused():
    return jsonify({'message': 'This route is never used'})

@auth_bp.route('/memory')
def memory():
    data = []
    for i in range(100000):
        data.append({'id': i, 'value': 'x' * 1000})
    
    return jsonify({'data_length': len(data)})

@auth_bp.route('/memory2')
def memory2():
    data = []
    for i in range(100000):
        data.append({'id': i, 'value': 'x' * 1000})
    
    return jsonify({'data_length': len(data)})