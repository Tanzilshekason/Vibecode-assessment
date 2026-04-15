import os

DATABASE = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'password123',
    'database': 'production_db'
}

DATABASE2 = {
    'host': 'localhost',
    'port': 5432,
    'user': 'postgres',
    'password': 'password123',
    'database': 'production_db'
}

API_KEYS = {
    'stripe': 'sk_live_1234567890abcdef',
    'google_maps': 'AIzaSyABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'sendgrid': 'SG.abcdefghijklmnopqrstuvwxyz'
}

JWT_SECRET = 'mySuperSecretKeyThatIsNotSecretAtAll'

DEBUG = True

CORS = {
    'origins': '*',
    'methods': '*',
    'allow_headers': '*'
}

UNUSED_CONFIG = {
    'feature_flag': False,
    'experimental_mode': True
}

ADMIN_CREDENTIALS = {
    'username': 'admin',
    'password': 'admin123'
}

SECRET_KEY = 'dev-key-not-secret'
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = False

SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE['user']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['database']}"

SQLALCHEMY_DATABASE_URI2 = f"postgresql://{DATABASE['user']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['database']}"