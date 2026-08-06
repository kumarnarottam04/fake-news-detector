import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

class Config:
    """Base application configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-fake-news-detector-key-2026')
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1 MB max payload
    
    # Model Artifact Paths
    MODEL_PATH = BASE_DIR / os.getenv('MODEL_PATH', 'models/model.joblib')
    VECTORIZER_PATH = BASE_DIR / os.getenv('VECTORIZER_PATH', 'models/tfidf_vectorizer.joblib')
    
    # Directories
    DATA_DIR = BASE_DIR / 'data'
    RAW_DATA_DIR = DATA_DIR / 'raw'
    PROCESSED_DATA_DIR = DATA_DIR / 'processed'
    SAMPLES_DIR = DATA_DIR / 'samples'
    LOGS_DIR = BASE_DIR / 'logs'
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = LOGS_DIR / 'app.log'

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    DEBUG = True
    TESTING = True

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    env = os.getenv('FLASK_ENV', 'development').lower()
    return config_by_name.get(env, DevelopmentConfig)
