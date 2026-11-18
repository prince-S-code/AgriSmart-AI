import json
import pickle
from pathlib import Path
import numpy as np

FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
MODEL_PATH = Path(__file__).resolve().parents[2] / "trained_models" / "crop" / "crop_model.pkl"


class CropService:
    def __init__(self):
        self.model = None
        self._load()

    def _load(self):
        if MODEL_PATH.exists():
            with MODEL_PATH.open("rb") as file:
                self.model = pickle.load(file)

    def is_available(self) -> bool:
        return self.model is not None

    def predict(self, values: dict):
        if not self.is_available():
            raise RuntimeError("Crop model not found. Run the crop training script first.")
        row = np.array([[values[name] for name in FEATURES]], dtype=float)
        probabilities = getattr(self.model, "predict_proba", lambda _: None)(row)
        if probabilities is None:
            classes = getattr(self.model, "classes_", [self.model.predict(row)[0]])
            scores = [1.0 if c == classes else 0.0 for c in classes]
        else:
            classes = self.model.classes_
            scores = probabilities[0]
        ranked = sorted(zip(classes.tolist(), scores.tolist()), key=lambda item: item[1], reverse=True)
        top = ranked[:3]
        return {
            "recommended_crop": top[0][0],
            "alternatives": [{"crop": crop, "score": round(float(score), 4)} for crop, score in top],
            "model_used": "RandomForestClassifier",
        }


crop_service = CropService()
