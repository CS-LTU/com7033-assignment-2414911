
"""
Main Flask application entry point.
Initializes the application, database, authentication, and routes.
"""

from flask import Flask, render_template
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect, generate_csrf
from routes.auth_routes import auth_bp
from routes.patient_routes import patient_bp
from models.auth_model import init_auth_db, User
from config import Config

def create_app():
    """
    Application factory function to create and configure the Flask app.
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)

    # Initialize CSRF protection for form security
    csrf = CSRFProtect(app)
    
    # Make CSRF token available in all templates
    @app.context_processor
    def inject_csrf_token():
        def csrf_token():
            return generate_csrf()
        return dict(csrf_token=csrf_token)

    # Initialize authentication database
    init_auth_db()

    # Configure Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        """
        Load user from database for Flask-Login session management.
        
        Args:
            user_id: User ID from session
            
        Returns:
            User object or None
        """
        return User.get_by_id(user_id)

    @app.route("/")
    def home():
        """
        Home page route.
        """
        return render_template("home.html")

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(patient_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
