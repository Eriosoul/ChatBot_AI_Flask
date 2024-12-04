import secrets

class Config:
    SECRET_KEY = secrets.token_hex(16)
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = 'password'
    DB_NAME = 'chatbot'
