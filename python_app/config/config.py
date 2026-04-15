import os
from dotenv import load_dotenv

load_dotenv()

DATABASE = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'production_db')
}

API_KEYS = {
    'stripe': os.getenv('STRIPE_API_KEY', ''),
    'google_maps': os.getenv('GOOGLE_MAPS_API_KEY', ''),
    'sendgrid': os.getenv('SENDGRID_API_KEY', '')
}

JWT_SECRET = os.getenv('JWT_SECRET', 'change-this-in-production')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

CORS = {
    'origins': os.getenv('CORS_ORIGINS', '*').split(','),
    'methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    'allow_headers': ['Content-Type', 'Authorization']
}

ADMIN_CREDENTIALS = {
    'username': os.getenv('ADMIN_USERNAME', 'admin'),
    'password': os.getenv('ADMIN_PASSWORD', '')
}

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
SESSION_COOKIE_HTTPONLY = True

SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE['user']}:{DATABASE['password']}@{DATABASE['host']}:{DATABASE['port']}/{DATABASE['database']}"