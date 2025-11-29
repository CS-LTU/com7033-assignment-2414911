"""
Unit tests for patient management functionality.
Tests patient CRUD operations and validation.
"""

import pytest
from models.patient_model import create_patient, get_all_patients, get_patient, update_patient, delete_patient
from utils.validation import validate_patient_name, validate_patient_age, validate_object_id
from bson import ObjectId


class TestPatientValidation:
    """Test cases for patient data validation."""
    
    def test_validate_patient_name_valid(self):
        """Test validation of valid patient names."""
        valid, error = validate_patient_name("John Doe")
        assert valid is True
        assert error == ""
        
        valid, error = validate_patient_name("Mary-Jane O'Connor")
        assert valid is True
        
        valid, error = validate_patient_name("Li")
        assert valid is True
    
    def test_validate_patient_name_invalid(self):
        """Test validation of invalid patient names."""
        # Empty name
        valid, error = validate_patient_name("")
        assert valid is False
        assert "required" in error.lower()
        
        # Too short
        valid, error = validate_patient_name("A")
        assert valid is False
        assert "2 characters" in error
        
        # Invalid characters
        valid, error = validate_patient_name("John123")
        assert valid is False
        assert "letters" in error.lower()
    
    def test_validate_patient_age_valid(self):
        """Test validation of valid patient ages."""
        valid, error, age = validate_patient_age("25")
        assert valid is True
        assert error == ""
        assert age == 25
        
        valid, error, age = validate_patient_age("0")
        assert valid is True
        assert age == 0
        
        valid, error, age = validate_patient_age("150")
        assert valid is True
        assert age == 150
    
    def test_validate_patient_age_invalid(self):
        """Test validation of invalid patient ages."""
        # Empty age
        valid, error, age = validate_patient_age("")
        assert valid is False
        assert "required" in error.lower()
        assert age is None
        
        # Not a number
        valid, error, age = validate_patient_age("abc")
        assert valid is False
        assert "number" in error.lower()
        assert age is None
        
        # Negative age
        valid, error, age = validate_patient_age("-5")
        assert valid is False
        assert "negative" in error.lower()
        
        # Too large
        valid, error, age = validate_patient_age("200")
        assert valid is False
        assert "150" in error
    
    def test_validate_object_id(self):
        """Test validation of MongoDB ObjectId."""
        # Valid ObjectId
        valid_id = str(ObjectId())
        valid, error = validate_object_id(valid_id)
        assert valid is True
        assert error == ""
        
        # Invalid ObjectId
        valid, error = validate_object_id("invalid")
        assert valid is False
        assert "invalid" in error.lower()
        
        # Empty ID
        valid, error = validate_object_id("")
        assert valid is False
        assert "required" in error.lower()

