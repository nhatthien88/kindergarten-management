
import os 
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

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_ECHO = True  # Show SQL queries in console

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}