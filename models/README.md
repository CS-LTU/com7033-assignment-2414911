# Models Directory

This directory contains the trained machine learning model for stroke prediction.

## Model File

Place your trained model file here with the filename: **`stroke_model.pkl`**

## Model Requirements

The model should be:
- A pickle file (`.pkl`) containing a trained scikit-learn model
- Compatible with scikit-learn's `predict()` and `predict_proba()` methods
- Trained to accept the following features in order:
  1. gender (numeric: 0=Female, 1=Male, 2=Other)
  2. age (numeric)
  3. hypertension (numeric: 0=No, 1=Yes)
  4. ever_married (numeric: 0=No, 1=Yes)
  5. work_type (numeric: 0=Private, 1=Self-employed, 2=Govt_job, 3=Children, 4=Never_worked)
  6. residence_type (numeric: 0=Rural, 1=Urban)
  7. avg_glucose_level (numeric)
  8. bmi (numeric)
  9. smoking_status (numeric: 0=Never smoked, 1=Unknown, 2=Formerly smoked, 3=Smokes)

## Model Output

The model should output:
- Binary classification: 0 (No stroke) or 1 (Stroke)
- Optional: Probability scores via `predict_proba()` method

## Example Model Training

```python
import pickle
from sklearn.ensemble import RandomForestClassifier

# Train your model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the model
with open('models/stroke_model.pkl', 'wb') as f:
    pickle.dump(model, f)
```

