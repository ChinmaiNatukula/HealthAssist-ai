import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'healthassist-secret-key-2024')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///healthassist.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-healthassist-secret-2024')
    JWT_ACCESS_TOKEN_EXPIRES = False  # tokens don't expire for demo
