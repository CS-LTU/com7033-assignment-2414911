
"""
Configuration settings for the Stroke Secure application.
Manages database connections and security keys.
"""

import os

class Config:
    """
    Application configuration class.
    Contains settings for Flask app, databases, and security.
    """
    # Secret key for session management and CSRF protection
    # In production, this should be set via environment variable
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
    
    # MongoDB connection URI for patient records
    MONGO_URI = os.environ.get('MONGO_URI') or "mongodb://localhost:27017/stroke_db"
    
    # SQLite database path for user authentication
    SQLALCHEMY_DB = "instance/auth.db"
    
    # CSRF protection settings
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None
