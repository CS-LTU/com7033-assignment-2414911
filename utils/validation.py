"""
Input validation utilities for the Stroke Secure application.
Provides validation functions for user authentication and patient data.
"""

import re
from bson import ObjectId


def validate_username(username):
    """
    Validate username format.
    
    Args:
        username: Username string to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if not username:
        return False, "Username is required"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters long"
    
    return True, ""


def validate_password(password):
    """
    Validate password strength.
    
    Args:
        password: Password string to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    if len(password) > 100:
        return False, "Password is too long"
    
    return True, ""


def validate_patient_name(name):
    """
    Validate patient name.
    
    Args:
        name: Patient name string to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if not name:
        return False, "Patient name is required"
    
    if len(name) < 2:
        return False, "Name must be at least 2 characters long"
    
    if len(name) > 100:
        return False, "Name is too long"
    
    # Allow letters, spaces, hyphens, and apostrophes
    if not re.match(r'^[a-zA-Z\s\-\']+$', name.strip()):
        return False, "Name can only contain letters, spaces, hyphens, and apostrophes"
    
    return True, ""


def validate_patient_age(age):
    """
    Validate patient age.
    
    Args:
        age: Age value to validate (can be string or int)
        
    Returns:
        tuple: (is_valid: bool, error_message: str, age_int: int or None)
    """
    if not age:
        return False, "Age is required", None
    
    try:
        age_int = int(age)
    except (ValueError, TypeError):
        return False, "Age must be a valid number", None
    
    if age_int < 0:
        return False, "Age cannot be negative", None
    
    if age_int > 150:
        return False, "Age must be a reasonable value (less than 150)", None
    
    return True, "", age_int


def validate_object_id(oid):
    """
    Validate MongoDB ObjectId format.
    
    Args:
        oid: ObjectId string to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if not oid:
        return False, "ID is required"
    
    if not ObjectId.is_valid(oid):
        return False, "Invalid patient ID format"
    
    return True, ""


def validate_gender(gender):
    """
    Validate gender value.
    
    Args:
        gender: Gender string to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    valid_genders = ["Male", "Female", "Other"]
    if gender not in valid_genders:
        return False, f"Gender must be one of: {', '.join(valid_genders)}"
    return True, ""


def validate_hypertension(hypertension):
    """
    Validate hypertension value.
    
    Args:
        hypertension: Hypertension value (can be string or int)
        
    Returns:
        tuple: (is_valid: bool, error_message: str, value_int: int or None)
    """
    if hypertension is None or hypertension == "":
        return False, "Hypertension value is required", None
    
    try:
        value_int = int(hypertension)
        if value_int not in [0, 1]:
            return False, "Hypertension must be 0 (No) or 1 (Yes)", None
        return True, "", value_int
    except (ValueError, TypeError):
        return False, "Hypertension must be 0 (No) or 1 (Yes)", None


def validate_ever_married(ever_married):
    """
    Validate ever_married value.
    
    Args:
        ever_married: Ever married string to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    valid_values = ["No", "Yes"]
    if ever_married not in valid_values:
        return False, f"Ever married must be one of: {', '.join(valid_values)}"
    return True, ""


def validate_work_type(work_type):
    """
    Validate work_type value.
    
    Args:
        work_type: Work type string to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    valid_types = ["Children", "Govt_job", "Never_worked", "Private", "Self-employed"]
    if work_type not in valid_types:
        return False, f"Work type must be one of: {', '.join(valid_types)}"
    return True, ""


def validate_residence_type(residence_type):
    """
    Validate residence_type value.
    
    Args:
        residence_type: Residence type string to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    valid_types = ["Rural", "Urban"]
    if residence_type not in valid_types:
        return False, f"Residence type must be one of: {', '.join(valid_types)}"
    return True, ""


def validate_avg_glucose_level(glucose_level):
    """
    Validate average glucose level.
    
    Args:
        glucose_level: Glucose level value (can be string or float)
        
    Returns:
        tuple: (is_valid: bool, error_message: str, value_float: float or None)
    """
    if not glucose_level:
        return False, "Average glucose level is required", None
    
    try:
        value_float = float(glucose_level)
        if value_float < 0:
            return False, "Glucose level cannot be negative", None
        if value_float > 500:
            return False, "Glucose level must be a reasonable value (less than 500)", None
        return True, "", value_float
    except (ValueError, TypeError):
        return False, "Glucose level must be a valid number", None


def validate_bmi(bmi):
    """
    Validate BMI value.
    
    Args:
        bmi: BMI value (can be string or float)
        
    Returns:
        tuple: (is_valid: bool, error_message: str, value_float: float or None)
    """
    if not bmi:
        return False, "BMI is required", None
    
    try:
        value_float = float(bmi)
        if value_float < 0:
            return False, "BMI cannot be negative", None
        if value_float > 100:
            return False, "BMI must be a reasonable value (less than 100)", None
        return True, "", value_float
    except (ValueError, TypeError):
        return False, "BMI must be a valid number", None


def validate_smoking_status(smoking_status):
    """
    Validate smoking_status value.
    
    Args:
        smoking_status: Smoking status string to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    valid_statuses = ["Formerly smoked", "Never smoked", "Smokes", "Unknown"]
    if smoking_status not in valid_statuses:
        return False, f"Smoking status must be one of: {', '.join(valid_statuses)}"
    return True, ""

