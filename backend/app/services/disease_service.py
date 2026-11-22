import json
from pathlib import Path
from PIL import Image
import numpy as np
from app.services.disease_treatments import get_treatment

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = BASE_DIR / "trained_models" / "disease"
MODEL_PATH = MODEL_DIR / "plant_disease_model.keras"
METADATA_PATH = MODEL_DIR / "metadata.json"


class DiseaseService:
    def __init__(self):
        self.model = None
        self.metadata = None

    def is_available(self) -> bool:
        return MODEL_PATH.exists() and METADATA_PATH.exists()

    def _load(self):
        if self.model is not None:
            return
        if not self.is_available():
            raise RuntimeError("Disease model artifact or metadata is missing")
        import tensorflow as tf
        self.metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
        self.model = tf.keras.models.load_model(MODEL_PATH, compile=False)

    def predict(self, image_path: Path):
        self._load()
        import tensorflow as tf
        size = tuple(self.metadata.get("image_size", [224, 224]))
        with Image.open(image_path) as image:
            image.verify()
        with Image.open(image_path) as image:
            rgb = image.convert("RGB")
            rgb = rgb.resize(size)
            array = tf.keras.utils.img_to_array(rgb)
            array = tf.keras.applications.mobilenet_v2.preprocess_input(array)
        probabilities = self.model.predict(np.expand_dims(array, axis=0), verbose=0)[0]
        index = int(np.argmax(probabilities))
        classes = self.metadata["class_names"]
        if index >= len(classes):
            raise RuntimeError("Disease model output does not match class metadata")
        class_name = classes[index]
        treatment = get_treatment(class_name)
        return {
            "crop_name": class_name.split("___", 1)[0].replace("_", " "),
            "predicted_disease": class_name,
            "confidence": round(float(probabilities[index]), 4),
            "test_accuracy": self.metadata.get("test_accuracy"),
            "model_used": self.metadata["model_name"],
            "low_confidence": float(probabilities[index]) < 0.60,
            "description": treatment["description"],
            "severity": treatment["severity"],
            "treatment_steps": treatment["steps"],
        }


disease_service = DiseaseService()
