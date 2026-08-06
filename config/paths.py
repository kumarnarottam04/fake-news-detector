"""
Centralized Filesystem Path Resolvers
"""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Data Directories
DATA_DIR = BASE_DIR / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
INTERIM_DATA_DIR = DATA_DIR / 'interim'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'
EXTERNAL_DATA_DIR = DATA_DIR / 'external'
VALIDATION_DATA_DIR = DATA_DIR / 'validation'

# Models & Artifacts
MODELS_DIR = BASE_DIR / 'models'
TRAINED_MODELS_DIR = MODELS_DIR / 'trained'
VECTORIZERS_DIR = MODELS_DIR / 'vectorizers'
MODEL_METADATA_DIR = MODELS_DIR / 'metadata'

ARTIFACTS_DIR = BASE_DIR / 'artifacts'
LOGS_DIR = BASE_DIR / 'logs'
DOCS_DIR = BASE_DIR / 'docs'
