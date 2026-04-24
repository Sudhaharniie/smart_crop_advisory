import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///crop_advisory.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API Keys (Replace with actual keys)
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')
    GOOGLE_TRANSLATE_API_KEY = os.environ.get('GOOGLE_TRANSLATE_API_KEY')
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Upload folder for images
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Supported languages
    LANGUAGES = {
        'en': 'English',
        'hi': 'हिन्दी',
        'bn': 'বাংলা',
        'te': 'తెలుగు',
        'ta': 'தமிழ்',
        'gu': 'ગુજરાતી',
        'mr': 'मराठी',
        'kn': 'ಕನ್ನಡ'
    }
