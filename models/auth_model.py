
"""
Authentication model for user management using SQLite database.
Handles user creation, authentication, and password hashing.
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

DEFAULT_DB_PATH = os.path.join("instance", "auth.db")
os.makedirs(os.path.dirname(DEFAULT_DB_PATH), exist_ok=True)
DB_PATH = DEFAULT_DB_PATH
def set_db_path(path):
    """
    Update the database path used by the authentication model.

    Args:
        path: Filesystem path to the SQLite database.
    """
    global DB_PATH
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    DB_PATH = path


def init_auth_db():
    """
    Initialize the SQLite database for user authentication.
    Creates the users table if it doesn't exist.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )""")
    conn.commit()
    conn.close()


class User(UserMixin):
    """
    User model for authentication.
    Implements Flask-Login's UserMixin for session management.
    """
    
    def __init__(self, id, username, password):
        """
        Initialize a User instance.
        
        Args:
            id: User ID
            username: Username
            password: Hashed password
        """
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def create(username, password):
        """
        Create a new user with hashed password.
        
        Args:
            username: Username for the new user
            password: Plain text password (will be hashed)
            
        Returns:
            bool: True if user was created successfully, False otherwise
        """
        try:
            hashed = generate_password_hash(password)
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("INSERT INTO users(username,password) VALUES(?,?)", (username, hashed))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            # Username already exists
            return False
        except Exception:
            return False

    @staticmethod
    def authenticate(username, password):
        """
        Authenticate a user by username and password.
        
        Args:
            username: Username to authenticate
            password: Plain text password to verify
            
        Returns:
            User object if authentication succeeds, None otherwise
        """
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT id,username,password FROM users WHERE username=?", (username,))
            row = c.fetchone()
            conn.close()
            
            if row and check_password_hash(row[2], password):
                return User(*row)
            return None
        except Exception:
            return None

    @staticmethod
    def get_by_id(uid):
        """
        Retrieve a user by their ID.
        
        Args:
            uid: User ID to look up
            
        Returns:
            User object if found, None otherwise
        """
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT id,username,password FROM users WHERE id=?", (uid,))
            row = c.fetchone()
            conn.close()
            return User(*row) if row else None
        except Exception:
            return None

    @staticmethod
    def username_exists(username):
        """
        Check if a username already exists in the database.
        
        Args:
            username: Username to check
            
        Returns:
            bool: True if username exists, False otherwise
        """
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT id FROM users WHERE username=?", (username,))
            result = c.fetchone()
            conn.close()
            return result is not None
        except Exception:
            return False
