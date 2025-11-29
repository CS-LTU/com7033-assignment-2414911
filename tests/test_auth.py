"""
Unit tests for authentication functionality.
Tests user creation, authentication, and validation.
"""

import os

import pytest

from models.auth_model import DB_PATH, User, init_auth_db, set_db_path
from utils.validation import validate_username, validate_password


@pytest.fixture(scope="function")
def setup_db(tmp_path):
    """
    Setup a temporary test database before each test.
    """
    original_db_path = DB_PATH
    test_db_path = tmp_path / "auth_test.db"
    set_db_path(str(test_db_path))

    init_auth_db()

    yield

    set_db_path(original_db_path)

    if test_db_path.exists():
        try:
            os.remove(test_db_path)
        except PermissionError:
            pass


class TestUserModel:
    """Test cases for User model."""
    
    def test_user_creation(self, setup_db):
        """Test creating a new user."""
        result = User.create("testuser", "testpass123")
        assert result is True
        
        # Verify user exists
        user = User.authenticate("testuser", "testpass123")
        assert user is not None
        assert user.username == "testuser"
    
    def test_user_authentication_success(self, setup_db):
        """Test successful user authentication."""
        User.create("testuser", "testpass123")
        user = User.authenticate("testuser", "testpass123")
        
        assert user is not None
        assert user.username == "testuser"
        assert user.id is not None
    
    def test_user_authentication_failure(self, setup_db):
        """Test failed user authentication."""
        User.create("testuser", "testpass123")
        
        # Wrong password
        user = User.authenticate("testuser", "wrongpass")
        assert user is None
        
        # Non-existent user
        user = User.authenticate("nonexistent", "testpass123")
        assert user is None
    
    def test_duplicate_username(self, setup_db):
        """Test that duplicate usernames are not allowed."""
        User.create("testuser", "testpass123")
        result = User.create("testuser", "anotherpass")
        
        assert result is False
    
    def test_get_user_by_id(self, setup_db):
        """Test retrieving user by ID."""
        User.create("testuser", "testpass123")
        auth_user = User.authenticate("testuser", "testpass123")
        
        retrieved_user = User.get_by_id(auth_user.id)
        assert retrieved_user is not None
        assert retrieved_user.username == "testuser"
        assert retrieved_user.id == auth_user.id
    
    def test_username_exists(self, setup_db):
        """Test username existence check."""
        assert User.username_exists("testuser") is False
        
        User.create("testuser", "testpass123")
        assert User.username_exists("testuser") is True
        assert User.username_exists("nonexistent") is False


class TestInputValidation:
    """Test cases for input validation."""
    
    def test_validate_username_valid(self):
        """Test validation of valid usernames."""
        valid, error = validate_username("testuser")
        assert valid is True
        assert error == ""
        
        valid, error = validate_username("user123")
        assert valid is True
        
        valid, error = validate_username("user_name")
        assert valid is True
        
        # Usernames with special characters are now allowed
        valid, error = validate_username("user@name")
        assert valid is True
        
        valid, error = validate_username("user-name")
        assert valid is True
    
    def test_validate_username_invalid(self):
        """Test validation of invalid usernames."""
        # Empty username
        valid, error = validate_username("")
        assert valid is False
        assert "required" in error.lower()
        
        # Too short
        valid, error = validate_username("ab")
        assert valid is False
        assert "3 characters" in error
    
    def test_validate_password_valid(self):
        """Test validation of valid passwords."""
        valid, error = validate_password("password123")
        assert valid is True
        assert error == ""
        
        valid, error = validate_password("pass12")
        assert valid is True  # Minimum 6 characters
    
    def test_validate_password_invalid(self):
        """Test validation of invalid passwords."""
        # Empty password
        valid, error = validate_password("")
        assert valid is False
        assert "required" in error.lower()
        
        # Too short
        valid, error = validate_password("12345")
        assert valid is False
        assert "6 characters" in error
        
        # Too long
        valid, error = validate_password("a" * 101)
        assert valid is False
        assert "too long" in error.lower()

