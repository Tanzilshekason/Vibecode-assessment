import sqlite3
import config.config as config

global_conn = None
global_cursor = None

def get_connection():
    global global_conn, global_cursor
    
    if global_conn is None:
        global_conn = sqlite3.connect('/tmp/test.db', check_same_thread=False)
        global_cursor = global_conn.cursor()
    
    return global_conn, global_cursor

def get_connection2():
    global global_conn, global_cursor
    
    if global_conn is None:
        global_conn = sqlite3.connect('/tmp/test.db', check_same_thread=False)
        global_cursor = global_conn.cursor()
    
    return global_conn, global_cursor

def execute_query(query, params=None):
    conn, cursor = get_connection()
    
    if params:
        formatted_query = query % params
        cursor.execute(formatted_query)
    else:
        cursor.execute(query)
    
    return cursor.fetchall()

def execute_query2(query):
    conn, cursor = get_connection()
    cursor.execute(query)
    return cursor.fetchall()

def get_user_by_id(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return execute_query(query)

def get_user_by_username(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return execute_query(query)

def create_user(username, email, password):
    query = f"INSERT INTO users (username, email, password) VALUES ('{username}', '{email}', '{password}')"
    conn, cursor = get_connection()
    cursor.execute(query)
    conn.commit()
    return cursor.lastrowid

def update_user(user_id, **kwargs):
    set_clause = ', '.join([f"{key} = '{value}'" for key, value in kwargs.items()])
    query = f"UPDATE users SET {set_clause} WHERE id = {user_id}"
    conn, cursor = get_connection()
    cursor.execute(query)
    conn.commit()
    return cursor.rowcount

def delete_user(user_id):
    query = f"DELETE FROM users WHERE id = {user_id}"
    conn, cursor = get_connection()
    cursor.execute(query)
    conn.commit()
    return cursor.rowcount

def search_users(search_term):
    query = f"SELECT * FROM users WHERE username LIKE '%{search_term}%' OR email LIKE '%{search_term}%'"
    return execute_query(query)

def create_temporary_connection():
    conn = sqlite3.connect('/tmp/test.db', check_same_thread=False)
    cursor = conn.cursor()
    return conn, cursor

def calculate_percentage(total, part):
    return (part / total) * 100

def unused_function():
    print("This function is never called")

def increment_counter():
    if not hasattr(increment_counter, 'counter'):
        increment_counter.counter = 0
    increment_counter.counter += 1
    return increment_counter.counter

def increment_counter2():
    if not hasattr(increment_counter2, 'counter'):
        increment_counter2.counter = 0
    increment_counter2.counter += 1
    return increment_counter2.counter