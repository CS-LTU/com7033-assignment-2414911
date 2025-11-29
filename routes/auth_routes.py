
"""
Authentication routes for user login, registration, and logout.
Includes input validation and security features.
"""

from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_user, logout_user, current_user
from models.auth_model import User
from utils.validation import validate_username, validate_password

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login with input validation.
    """
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect("/patients")
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        # Validate input
        username_valid, username_error = validate_username(username)
        password_valid, password_error = validate_password(password)
        
        if not username_valid:
            flash(username_error, "danger")
            return render_template("login.html")
        
        if not password_valid:
            flash(password_error, "danger")
            return render_template("login.html")
        
        # Authenticate user
        user = User.authenticate(username, password)
        if user:
            login_user(user)
            flash("Login successful!", "success")
            return redirect("/patients")
        else:
            flash("Invalid username or password", "danger")
    
    return render_template("login.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """
    Handle user registration with input validation.
    """
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect("/patients")
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        # Validate input
        username_valid, username_error = validate_username(username)
        password_valid, password_error = validate_password(password)
        
        if not username_valid:
            flash(username_error, "danger")
            return render_template("register.html")
        
        if not password_valid:
            flash(password_error, "danger")
            return render_template("register.html")
        
        # Check if username already exists
        if User.username_exists(username):
            flash("Username already exists. Please choose another.", "danger")
            return render_template("register.html")
        
        # Create user
        if User.create(username, password):
            flash("Account created successfully! Please login.", "success")
            return redirect("/auth/login")
        else:
            flash("Error creating account. Please try again.", "danger")
    
    return render_template("register.html")


@auth_bp.route("/logout")
def logout():
    """
    Handle user logout.
    """
    logout_user()
    flash("You have been logged out successfully.", "info")
    return redirect("/auth/login")
