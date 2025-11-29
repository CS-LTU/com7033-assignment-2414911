"""
Machine learning inference helpers that mirror the preprocessing + model
pipeline defined in `modeltraining/Model_Training.ipynb`.
"""

from pathlib import Path
from typing import Dict, Tuple

import joblib
import pandas as pd

MODEL_PATH = Path("modeltraining/stroke_model.pkl")
# Require at least 75% probability before flagging a very high heart-attack risk
PREDICTION_THRESHOLD = 0.75


class StrokePredictor:
    """
    Loads the persisted scikit-learn pipeline and serves stroke predictions.
    """

    def __init__(self, model_path: Path = MODEL_PATH, threshold: float = PREDICTION_THRESHOLD):
        self.model_path = Path(model_path)
        self.threshold = threshold
        self.model = None

    def load_model(self) -> None:
        """
        Load the trained model pipeline from disk (lazy-loaded).
        """
        if self.model is not None:
            return

        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Model file not found at {self.model_path}. "
                "Please export stroke_model.pkl from the training notebook into modeltraining/."
            )

        try:
            self.model = joblib.load(self.model_path)
        except Exception as exc:  # pragma: no cover - guarded path
            raise FileNotFoundError(f"Error loading model: {exc}") from exc

    @staticmethod
    def _as_float(value, default: float = 0.0) -> float:
        try:
            return float(value)
        except (TypeError, ValueError):
            return default

    @staticmethod
    def _as_int(value, default: int = 0) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def prepare_features(self, patient_data: Dict) -> pd.DataFrame:
        """
        Convert Mongo patient document into the DataFrame the pipeline expects.
        """
        payload = {
            "gender": patient_data.get("gender"),
            "age": self._as_float(patient_data.get("age")),
            "hypertension": self._as_int(patient_data.get("hypertension")),
            "ever_married": patient_data.get("ever_married"),
            "work_type": patient_data.get("work_type"),
            # Training pipeline used a capitalized Residence_type column name.
            "Residence_type": patient_data.get("residence_type"),
            "avg_glucose_level": self._as_float(patient_data.get("avg_glucose_level")),
            "bmi": self._as_float(patient_data.get("bmi")),
            "smoking_status": patient_data.get("smoking_status"),
        }
        return pd.DataFrame([payload])

    def predict(self, patient_data: Dict) -> Tuple[int, float]:
        """
        Predict stroke probability for a stored patient profile.
        Returns the binary prediction (thresholded at 0.75) and the stroke probability.
        """
        self.load_model()
        features = self.prepare_features(patient_data)

        try:
            probability = float(self.model.predict_proba(features)[0][1])
        except AttributeError as exc:  # pragma: no cover - pipeline always exposes proba
            raise RuntimeError("Loaded model does not expose predict_proba") from exc

        prediction = 1 if probability >= self.threshold else 0
        return prediction, probability


# Global predictor instance for reuse across requests
_predictor = None


def get_predictor() -> StrokePredictor:
    """
    Provide a memoized predictor instance so we avoid reloading the model repeatedly.
    """
    global _predictor
    if _predictor is None:
        _predictor = StrokePredictor()
    return _predictor

