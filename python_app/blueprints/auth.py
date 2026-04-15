from flask import Blueprint, request, jsonify, session, g
import sqlite3
import bcrypt
import jwt
import os
from datetime import datetime
from config.config import JWT_SECRET, ADMIN_CREDENTIALS

auth_bp = Blueprint('auth', __name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(os.getenv('DB_PATH', '/tmp/test.db'))
        db.row_factory = sqlite3.Row
    return db

@auth_bp.teardown_app_request
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    
    if user:
        # Assume password is hashed with bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            token = jwt.encode({'user_id': user['id']}, JWT_SECRET, algorithm='HS256')
            session['user_id'] = user['id']
            return jsonify({'token': token})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@auth_bp.route('/admin/login', methods=['POST'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username == ADMIN_CREDENTIALS['username'] and password == ADMIN_CREDENTIALS['password']:
        session['is_admin'] = True
        return jsonify({'message': 'Admin logged in'})
    else:
        return jsonify({'error': 'Invalid admin credentials'}), 401

@auth_bp.route('/profile')
def profile():
    user_id = session.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    
    if user:
        return jsonify({
            'id': user['id'],
            'username': user['username'],
            'email': user['email']
        })
    else:
        return jsonify({'error': 'User not found'}), 404

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('is_admin', None)
    return jsonify({'message': 'Logged out'})

@auth_bp.route('/stats')
def stats():
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    # Assuming there is a last_login column; if not, fallback to total_users
    try:
        cursor.execute("SELECT COUNT(*) FROM users WHERE last_login > DATE('now', '-30 days')")
        active_users = cursor.fetchone()[0]
    except sqlite3.OperationalError:
        active_users = total_users
    
    percentage = (active_users / total_users) * 100 if total_users > 0 else 0
    
    return jsonify({
        'total_users': total_users,
        'active_users': active_users,
        'percentage': round(percentage, 2)
    })