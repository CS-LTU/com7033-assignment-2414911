
"""
Patient management routes for CRUD operations.
Includes input validation and error handling.
"""

from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required
from models.patient_model import create_patient, get_all_patients, get_patient, update_patient, delete_patient
from utils.validation import (
    validate_patient_name, validate_patient_age, validate_object_id,
    validate_gender, validate_hypertension, validate_ever_married,
    validate_work_type, validate_residence_type, validate_avg_glucose_level,
    validate_bmi, validate_smoking_status
)
from utils.model_predictor import get_predictor

patient_bp = Blueprint("patients", __name__, url_prefix="/patients")


@patient_bp.route("/")
@login_required
def list_patients():
    """
    Display list of all patients.
    """
    try:
        pts = get_all_patients()
        return render_template("patients/list.html", patients=pts)
    except Exception as e:
        flash("Error loading patients. Please try again.", "danger")
        return render_template("patients/list.html", patients=[])


@patient_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_patient():
    """
    Add a new patient with input validation.
    """
    if request.method == "POST":
        # Get and validate all form fields
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "")
        hypertension = request.form.get("hypertension", "")
        ever_married = request.form.get("ever_married", "")
        work_type = request.form.get("work_type", "")
        residence_type = request.form.get("residence_type", "")
        avg_glucose_level = request.form.get("avg_glucose_level", "").strip()
        bmi = request.form.get("bmi", "").strip()
        smoking_status = request.form.get("smoking_status", "")
        
        # Validate all inputs
        name_valid, name_error = validate_patient_name(name)
        age_valid, age_error, age_int = validate_patient_age(age)
        gender_valid, gender_error = validate_gender(gender)
        hypertension_valid, hypertension_error, hypertension_int = validate_hypertension(hypertension)
        ever_married_valid, ever_married_error = validate_ever_married(ever_married)
        work_type_valid, work_type_error = validate_work_type(work_type)
        residence_type_valid, residence_type_error = validate_residence_type(residence_type)
        glucose_valid, glucose_error, glucose_float = validate_avg_glucose_level(avg_glucose_level)
        bmi_valid, bmi_error, bmi_float = validate_bmi(bmi)
        smoking_valid, smoking_error = validate_smoking_status(smoking_status)
        
        # Check all validations
        if not name_valid:
            flash(name_error, "danger")
            return render_template("patients/add.html")
        if not age_valid:
            flash(age_error, "danger")
            return render_template("patients/add.html")
        if not gender_valid:
            flash(gender_error, "danger")
            return render_template("patients/add.html")
        if not hypertension_valid:
            flash(hypertension_error, "danger")
            return render_template("patients/add.html")
        if not ever_married_valid:
            flash(ever_married_error, "danger")
            return render_template("patients/add.html")
        if not work_type_valid:
            flash(work_type_error, "danger")
            return render_template("patients/add.html")
        if not residence_type_valid:
            flash(residence_type_error, "danger")
            return render_template("patients/add.html")
        if not glucose_valid:
            flash(glucose_error, "danger")
            return render_template("patients/add.html")
        if not bmi_valid:
            flash(bmi_error, "danger")
            return render_template("patients/add.html")
        if not smoking_valid:
            flash(smoking_error, "danger")
            return render_template("patients/add.html")
        
        # Create patient data dictionary
        patient_data = {
            "name": name,
            "age": age_int,
            "gender": gender,
            "hypertension": hypertension_int,
            "ever_married": ever_married,
            "work_type": work_type,
            "residence_type": residence_type,
            "avg_glucose_level": glucose_float,
            "bmi": bmi_float,
            "smoking_status": smoking_status
        }
        
        try:
            create_patient(patient_data)
            flash("Patient added successfully!", "success")
            return redirect("/patients")
        except Exception:
            flash("Error adding patient. Please try again.", "danger")
    
    return render_template("patients/add.html")


@patient_bp.route("/edit/<id>", methods=["GET", "POST"])
@login_required
def edit_patient(id):
    """
    Edit an existing patient with input validation.
    """
    # Validate patient ID
    id_valid, id_error = validate_object_id(id)
    if not id_valid:
        flash(id_error, "danger")
        return redirect("/patients")
    
    patient = get_patient(id)
    if not patient:
        flash("Patient not found.", "danger")
        return redirect("/patients")
    
    if request.method == "POST":
        # Get and validate all form fields
        name = request.form.get("name", "").strip()
        age = request.form.get("age", "").strip()
        gender = request.form.get("gender", "")
        hypertension = request.form.get("hypertension", "")
        ever_married = request.form.get("ever_married", "")
        work_type = request.form.get("work_type", "")
        residence_type = request.form.get("residence_type", "")
        avg_glucose_level = request.form.get("avg_glucose_level", "").strip()
        bmi = request.form.get("bmi", "").strip()
        smoking_status = request.form.get("smoking_status", "")
        
        # Validate all inputs
        name_valid, name_error = validate_patient_name(name)
        age_valid, age_error, age_int = validate_patient_age(age)
        gender_valid, gender_error = validate_gender(gender)
        hypertension_valid, hypertension_error, hypertension_int = validate_hypertension(hypertension)
        ever_married_valid, ever_married_error = validate_ever_married(ever_married)
        work_type_valid, work_type_error = validate_work_type(work_type)
        residence_type_valid, residence_type_error = validate_residence_type(residence_type)
        glucose_valid, glucose_error, glucose_float = validate_avg_glucose_level(avg_glucose_level)
        bmi_valid, bmi_error, bmi_float = validate_bmi(bmi)
        smoking_valid, smoking_error = validate_smoking_status(smoking_status)
        
        # Check all validations
        if not name_valid:
            flash(name_error, "danger")
            return render_template("patients/edit.html", patient=patient)
        if not age_valid:
            flash(age_error, "danger")
            return render_template("patients/edit.html", patient=patient)
        if not gender_valid:
            flash(gender_error, "danger")
            return render_template("patients/edit.html", patient=patient)
        if not hypertension_valid:
            flash(hypertension_error, "danger")
            return render_template("patients/edit.html", patient=patient)
        if not ever_married_valid:
            flash(ever_married_error, "danger")
            return render_template("patients/edit.html", patient=patient)
        if not work_type_valid:
            flash(work_type_error, "danger")
            return render_template("patients/edit.html", patient=patient)
        if not residence_type_valid:
            flash(residence_type_error, "danger")
            return render_template("patients/edit.html", patient=patient)
        if not glucose_valid:
            flash(glucose_error, "danger")
            return render_template("patients/edit.html", patient=patient)
        if not bmi_valid:
            flash(bmi_error, "danger")
            return render_template("patients/edit.html", patient=patient)
        if not smoking_valid:
            flash(smoking_error, "danger")
            return render_template("patients/edit.html", patient=patient)
        
        # Update patient data
        patient_data = {
            "name": name,
            "age": age_int,
            "gender": gender,
            "hypertension": hypertension_int,
            "ever_married": ever_married,
            "work_type": work_type,
            "residence_type": residence_type,
            "avg_glucose_level": glucose_float,
            "bmi": bmi_float,
            "smoking_status": smoking_status
        }
        
        try:
            result = update_patient(id, patient_data)
            if result and result.modified_count > 0:
                flash("Patient updated successfully!", "success")
            else:
                flash("No changes were made.", "info")
            return redirect("/patients")
        except Exception:
            flash("Error updating patient. Please try again.", "danger")
    
    return render_template("patients/edit.html", patient=patient)


@patient_bp.route("/delete/<id>")
@login_required
def delete(id):
    """
    Delete a patient record.
    """
    # Validate patient ID
    id_valid, id_error = validate_object_id(id)
    if not id_valid:
        flash(id_error, "danger")
        return redirect("/patients")
    
    try:
        result = delete_patient(id)
        if result and result.deleted_count > 0:
            flash("Patient deleted successfully!", "success")
        else:
            flash("Patient not found.", "danger")
    except Exception:
        flash("Error deleting patient. Please try again.", "danger")
    
    return redirect("/patients")


@patient_bp.route("/predict/<id>")
@login_required
def predict_stroke(id):
    """
    Predict stroke risk for a patient.
    """
    # Validate patient ID
    id_valid, id_error = validate_object_id(id)
    if not id_valid:
        flash(id_error, "danger")
        return redirect("/patients")
    
    # Get patient data
    patient = get_patient(id)
    if not patient:
        flash("Patient not found.", "danger")
        return redirect("/patients")
    
    try:
        # Get predictor and make prediction
        predictor = get_predictor()
        prediction, probability = predictor.predict(patient)
        
        # Convert prediction to readable format
        stroke_risk = "High Heart Attack Risk" if prediction == 1 else "Low Heart Attack Risk"
        stroke_probability_pct = probability * 100 if probability is not None else None
        
        return render_template(
            "patients/predict.html",
            patient=patient,
            prediction=prediction,
            stroke_risk=stroke_risk,
            probability=stroke_probability_pct,
        )
    
    except FileNotFoundError as e:
        flash("Model file not found. Please ensure the trained model is placed in the models/ directory.", "danger")
        return redirect("/patients")
    except Exception as e:
        flash(f"Error making prediction: {str(e)}", "danger")
        return redirect("/patients")
