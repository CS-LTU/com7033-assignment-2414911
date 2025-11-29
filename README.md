# Stroke Secure - Patient Management System

A fully functional web application for managing stroke patient records with enhanced security features and user-friendly interface.

## Features

- **Dual Database Architecture**: 
  - SQLite for secure user authentication
  - MongoDB for patient record storage
  
- **Security Features**:
  - Password hashing using Werkzeug
  - Input validation for all user inputs
  - CSRF protection for forms
  - Session-based authentication with Flask-Login
  
- **User Management**:
  - User registration with validation
  - Secure login/logout
  - Protected routes
  
- **Patient Management**:
  - Add new patient records
  - View all patients
  - Edit patient information
  - Delete patient records
  
- **Enhanced UI/UX**:
  - Modern Bootstrap 5 interface
  - Responsive design
  - Flash messages for user feedback
  - Intuitive navigation

## Technology Stack

- **Backend**: Flask (Python)
- **Databases**: SQLite, MongoDB
- **Authentication**: Flask-Login
- **Security**: Flask-WTF (CSRF), Werkzeug (Password Hashing)
- **Frontend**: Bootstrap 5, Jinja2 Templates
- **Testing**: pytest

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd stroke_secure
```

2. Create and activate a virtual environment (recommended):
```bash
# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
   - Copy `.env.example` to `.env` (if the file exists) or set the following variables in your shell:
     - `FLASK_ENV=development`
     - `SECRET_KEY=<random-string>`
     - `MONGO_URI=mongodb://localhost:27017/stroke_secure`
   - Update `config.py` if you prefer to hardcode the Mongo URI or other settings.

## Database Setup

1. **SQLite (Authentication)**
   - No manual steps required; `models/auth_model.py` ensures `instance/auth.db` exists and sets up the `users` table via `init_auth_db()`.
   - When running tests, `tests/test_auth.py` swaps to a temporary SQLite file automatically.

2. **MongoDB (Patients)**
   - Install and start MongoDB locally (default port `27017`).
     ```bash
     # Windows
     net start MongoDB

     # macOS (Homebrew)
     brew services start mongodb-community

     # Linux (systemd)
     sudo systemctl start mongod
     ```
   - Create the target database (optional; the app will create it lazily):
     ```bash
     mongosh
     use stroke_secure
     db.createCollection("patients")
     exit
     ```
   - If you use a cloud provider (e.g., MongoDB Atlas), update `MONGO_URI` in `config.py` or your environment variables accordingly.

## Running the Application

1. Ensure the virtual environment is active and MongoDB is running.
2. Initialize the SQLite DB (only needed the first time):
   ```bash
   python -c "from models.auth_model import init_auth_db; init_auth_db()"
   ```
3. Start the Flask server:
   ```bash
   python app.py
   ```
4. Open `http://localhost:5000` in your browser, register an account, and begin managing patients.

## Running Tests

```bash
pytest
```

```bash
# MongoDB should be running on localhost:27017
# Or update MONGO_URI in config.py
```

4. Run the application:
```bash
python app.py
```

5. Access the application:
- Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
stroke_secure/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── models/                # Data models
│   ├── auth_model.py      # User authentication model
│   └── patient_model.py   # Patient data model
├── routes/                # Route handlers
│   ├── auth_routes.py     # Authentication routes
│   └── patient_routes.py  # Patient management routes
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── home.html          # Home page
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   └── patients/          # Patient templates
├── utils/                 # Utility functions
│   └── validation.py      # Input validation functions
├── tests/                 # Unit tests
│   ├── test_auth.py       # Authentication tests
│   └── test_patient.py    # Patient validation tests
└── instance/              # Database files
    └── auth.db            # SQLite database
```

## File-by-File Overview

- `app.py`: Bootstraps the Flask application, registers blueprints, and configures extensions such as Flask-Login.
- `config.py`: Central configuration (secret keys, Mongo connection URI, and other runtime flags).
- `requirements.txt`: Exact Python package dependencies needed to run the project.
- `pytest.ini`: Pytest configuration that points the test runner at the `tests/` directory.
- `models/auth_model.py`: SQLite-powered authentication layer, including password hashing, user CRUD helpers, and a configurable DB path for tests.
- `models/patient_model.py`: MongoDB access helpers for creating, updating, listing, and deleting patient documents.
- `routes/auth_routes.py`: Handles registration, login, logout, and session protection.
- `routes/patient_routes.py`: Implements patient CRUD flows plus the `/predict/<id>` endpoint that invokes the ML model.
- `templates/base.html`: Global layout, navbar, and flash message handling.
- `templates/home.html`: Landing dashboard shown after login.
- `templates/login.html` / `templates/register.html`: Authentication forms with validation feedback.
- `templates/patients/list.html`: Table view of all patients with action buttons.
- `templates/patients/add.html` / `templates/patients/edit.html`: Forms for creating and updating patient profiles.
- `templates/patients/predict.html`: Explains the ML prediction result, visualizes probability, and highlights the 75% threshold.
- `utils/validation.py`: Shared input-validation helpers for usernames, passwords, patient demographics, and clinical metrics.
- `utils/model_predictor.py`: Lazy-loads the trained scikit-learn pipeline and exposes a `StrokePredictor` with a 0.75 high-risk threshold.
- `modeltraining/Model_Training.py` & `.ipynb`: Training pipeline, feature engineering, and exported `stroke_model.pkl`.
- `tests/test_auth.py`: Unit tests covering the authentication model, password validation rules, and fixture-backed database isolation.
- `tests/test_patient.py`: Tests patient input validators to ensure bad data is rejected.
- `instance/auth.db`: Default SQLite database file used in development (Pytest swaps it out with an isolated temp DB).
- `templates/base.html`, static assets, and Bootstrap imports provide a consistent, responsive UI.

## Running Tests

```bash
pytest
```

## Project Deliverables

This repository satisfies all requested deliverables:

1. **Fully functional web application**: `app.py`, the blueprints, and the Bootstrap-based templates provide an end-to-end experience with intuitive navigation and helpful flash messaging.
2. **Multiple databases**: `models/auth_model.py` uses SQLite for user credentials while `models/patient_model.py` talks to MongoDB for patient data, demonstrating dual-database integration.
3. **Secure create/update/delete flows**: `routes/patient_routes.py` and `models/patient_model.py` implement add, edit, and delete operations with rigorous validation, and the auth model enforces unique usernames plus hashed passwords.
4. **Security features**: Password hashing (Werkzeug) and comprehensive input validation (`utils/validation.py`) guard both authentication and patient forms; CSRF protection is enabled via Flask-WTF.
5. **Code documentation**: Functions and modules include docstrings/comments explaining intent, especially in validation, model prediction, and the auth model.
6. **Automated tests**: `tests/test_auth.py` and `tests/test_patient.py` provide Pytest coverage to verify both authentication and validation logic.

## Security Features

1. **Password Hashing**: All passwords are hashed using Werkzeug's secure password hashing
2. **Input Validation**: Comprehensive validation for:
   - Username (3-20 chars, alphanumeric + underscore)
   - Password (minimum 6 characters)
   - Patient name (letters, spaces, hyphens, apostrophes)
   - Patient age (0-150, numeric only)
   - ObjectId validation for MongoDB operations

## Database Operations

- **SQLite (Authentication)**: Secure user credentials storage
- **MongoDB (Patients)**: Flexible document storage for patient records

## License

This project is developed for educational purposes.

## Author

Developed as part of a secure web application project demonstrating:
- Multiple database integration
- Security best practices
- Input validation
- User authentication
- CRUD operations
