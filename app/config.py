
import os 
from datetime import timedelta
from dotenv import load_dotenv
"""os: de doc bien moi truong"""
"""dotenv: de load file .env"""
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    """tat di de toi uu hieu suat"""
    SQLALCHEMY_ECHO = False
    """TRUE IF Debugging"""

    SESSION_TYPE = 'filesystem' 
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7) 
    SESSION_COOKIE_SECURE = False 
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_NAME = 'kindergarten_session'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    SQLALCHEMY_ECHO = True 

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = 86400 
    JWT_REFRESH_TOKEN_EXPIRES = 2592000

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    SESSION_COOKIE_SECURE = True 

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}