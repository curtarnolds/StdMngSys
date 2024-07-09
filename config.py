"""File for configuration settings"""
import os

class Config:
    """
    Configuration class.
    Use secret key and database uri from environment if available.
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'oS_1c7P9d_P0u1gpqIlswXhX7nDr0c6ErOaN0BK7IRpGX569xru1lmwRnG4Wher62hEjchlKxXPzGLBX3ZUaoA'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///stdmgtsys.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
