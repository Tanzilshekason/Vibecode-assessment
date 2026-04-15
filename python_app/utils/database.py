import sqlite3
import os

global_conn = None
global_cursor = None

def get_connection():
    global global_conn, global_cursor
    
    if global_conn is None:
        global_conn = sqlite3.connect(os.getenv('DB_PATH', '/tmp/test.db'), check_same_thread=False)
        global_cursor = global_conn.cursor()
    
    return global_conn, global_cursor

def execute_query(query, params=None):
    conn, cursor = get_connection()
    
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    
    return cursor.fetchall()

def get_user_by_id(user_id):
    query = "SELECT * FROM users WHERE id = ?"
    return execute_query(query, (user_id,))

def get_user_by_username(username):
    query = "SELECT * FROM users WHERE username = ?"
    return execute_query(query, (username,))

def create_user(username, email, password):
    query = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)"
    conn, cursor = get_connection()
    cursor.execute(query, (username, email, password))
    conn.commit()
    return cursor.lastrowid

def update_user(user_id, **kwargs):
    set_clause = ', '.join([f"{key} = ?" for key in kwargs.keys()])
    query = f"UPDATE users SET {set_clause} WHERE id = ?"
    params = list(kwargs.values()) + [user_id]
    conn, cursor = get_connection()
    cursor.execute(query, params)
    conn.commit()
    return cursor.rowcount

def delete_user(user_id):
    query = "DELETE FROM users WHERE id = ?"
    conn, cursor = get_connection()
    cursor.execute(query, (user_id,))
    conn.commit()
    return cursor.rowcount

def search_users(search_term):
    query = "SELECT * FROM users WHERE username LIKE ? OR email LIKE ?"
    pattern = f'%{search_term}%'
    return execute_query(query, (pattern, pattern))

def create_temporary_connection():
    conn = sqlite3.connect(os.getenv('DB_PATH', '/tmp/test.db'), check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor

def calculate_percentage(total, part):
    return (part / total) * 100 if total != 0 else 0