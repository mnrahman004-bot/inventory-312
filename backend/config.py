"""
Configuration Settings for Inventory Management System
"""
import os
from datetime import timedelta

class Config:
    """Base configuration"""
    
    # Flask Settings
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    TESTING = False
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///../database/inventory.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv(
        'JWT_SECRET_KEY',
        'change-me-in-production-super-secret-key-min-32-chars-long'
    )
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', '2592000'))
    )
    
    # Application Settings
    MAX_PRODUCTS_PER_PAGE = int(os.getenv('MAX_PRODUCTS_PER_PAGE', '20'))
    
    # ML/Prediction Settings
    HISTORICAL_DAYS = int(os.getenv('HISTORICAL_DAYS', '90'))
    PREDICTION_DAYS = int(os.getenv('PREDICTION_DAYS', '7'))
    LEAD_TIME_DAYS = int(os.getenv('LEAD_TIME_DAYS', '3'))
    SAFETY_STOCK_DAYS = int(os.getenv('SAFETY_STOCK_DAYS', '2'))
    
    # CORS Settings
    CORS_ORIGINS = os.getenv(
        'ALLOWED_ORIGINS',
        'http://localhost:5000,http://localhost:3000'
    ).split(',')


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')  # Must be set
    
    if not JWT_SECRET_KEY:
        raise ValueError('JWT_SECRET_KEY environment variable is required in production')


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_SECRET_KEY = 'test-secret-key'


# Get config based on environment
config_type = os.getenv('FLASK_ENV', 'development').lower()

if config_type == 'production':
    current_config = ProductionConfig()
elif config_type == 'testing':
    current_config = TestingConfig()
else:
    current_config = DevelopmentConfig()
