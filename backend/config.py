"""
Configuration file for StudySaarthi Application
Handles environment variables and settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_ENABLED = os.getenv('OPENAI_ENABLED', 'true').strip().lower() in ('1', 'true', 'yes', 'on')

# Flask Configuration
FLASK_ENV = os.getenv('FLASK_ENV', 'development')
DEBUG = FLASK_ENV == 'development'
SECRET_KEY = os.getenv('SECRET_KEY', 'studysaarthi-secret-key')

# Data Storage Configuration
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
PROGRESS_FILE = os.path.join(DATA_DIR, 'progress.json')
SESSIONS_FILE = os.path.join(DATA_DIR, 'sessions.json')

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Agent Configuration
TOPIC_CATEGORIES = {
    'science_math': {
        'keywords': ['physics', 'chemistry', 'biology', 'mathematics', 'calculus', 'algebra', 'geometry', 'science'],
        'depth_level': 'detailed'
    },
    'history_gk': {
        'keywords': ['history', 'geography', 'politics', 'culture', 'heritage', 'dynasty', 'war', 'revolution'],
        'depth_level': 'contextual'
    },
    'general': {
        'keywords': ['technology', 'art', 'literature', 'music', 'sports', 'entertainment', 'health'],
        'depth_level': 'balanced'
    }
}

# Model Configuration
MODEL_CONFIG = {
    'model': 'gpt-3.5-turbo',
    'temperature': 0.7,
    'max_tokens': 1500,
    'top_p': 0.9
}
