
"""
Patient model for managing patient records in MongoDB.
Handles CRUD operations for patient data.
"""

from pymongo import MongoClient
from bson.objectid import ObjectId
from config import Config

# Initialize MongoDB connection
client = MongoClient(Config.MONGO_URI)
db = client["stroke_db"]
patients = db["patients"]


def create_patient(data):
    """
    Create a new patient record in MongoDB.
    
    Args:
        data: Dictionary containing patient information
        
    Returns:
        InsertOneResult object with the inserted document ID
    """
    return patients.insert_one(data)


def get_all_patients():
    """
    Retrieve all patient records from MongoDB.
    
    Returns:
        List of patient documents
    """
    return list(patients.find())


def get_patient(pid):
    """
    Retrieve a single patient by ID.
    
    Args:
        pid: Patient ID (ObjectId string)
        
    Returns:
        Patient document if found, None otherwise
    """
    try:
        return patients.find_one({"_id": ObjectId(pid)})
    except Exception:
        return None


def update_patient(pid, data):
    """
    Update a patient record in MongoDB.
    
    Args:
        pid: Patient ID (ObjectId string)
        data: Dictionary containing fields to update
        
    Returns:
        UpdateResult object
    """
    try:
        return patients.update_one({"_id": ObjectId(pid)}, {"$set": data})
    except Exception:
        return None


def delete_patient(pid):
    """
    Delete a patient record from MongoDB.
    
    Args:
        pid: Patient ID (ObjectId string)
        
    Returns:
        DeleteResult object
    """
    try:
        return patients.delete_one({"_id": ObjectId(pid)})
    except Exception:
        return None
