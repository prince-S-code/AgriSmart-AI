import json
from pathlib import Path

import numpy as np
from PIL import Image

from app.services.disease_treatments import get_treatment

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_DIR = BASE_DIR / "trained_models" / "disease"
TFLITE_MODEL_PATH = MODEL_DIR / "plant_disease_model.tflite"
METADATA_PATH = MODEL_DIR / "metadata.json"


class DiseaseService:
    def __init__(self):
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.metadata = None

    def is_available(self) -> bool:
        return TFLITE_MODEL_PATH.exists() and METADATA_PATH.exists()

    def _load(self):
        if self.interpreter is not None:
            return
        if not self.is_available():
            raise RuntimeError("Disease model artifact or metadata is missing")

        from ai_edge_litert.interpreter import Interpreter

        self.metadata = json.loads(METADATA_PATH.read_text(encoding="utf-8"))
        self.interpreter = Interpreter(
            model_path=str(TFLITE_MODEL_PATH),
            num_threads=2,
        )
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()[0]
        self.output_details = self.interpreter.get_output_details()[0]

    def predict(self, image_path: Path):
        self._load()

        size = tuple(self.metadata.get("image_size", [224, 224]))
        with Image.open(image_path) as image:
            image.verify()
        with Image.open(image_path) as image:
            rgb = image.convert("RGB")
            rgb = rgb.resize(size)
            array = np.asarray(rgb, dtype=np.float32)
            array = array / 127.5 - 1.0
        self.interpreter.set_tensor(
            self.input_details["index"],
            np.expand_dims(array, axis=0),
        )
        self.interpreter.invoke()
        probabilities = self.interpreter.get_tensor(
            self.output_details["index"]
        )[0]
        index = int(np.argmax(probabilities))
        classes = self.metadata["class_names"]
        if index >= len(classes):
            raise RuntimeError("Disease model output does not match class metadata")
        class_name = classes[index]
        confidence = float(probabilities[index])
        treatment = get_treatment(class_name)
        return {
            "crop_name": class_name.split("___", 1)[0].replace("_", " "),
            "predicted_disease": class_name,
            "confidence": round(confidence, 4),
            "test_accuracy": self.metadata.get("test_accuracy"),
            "model_used": self.metadata["model_name"],
            "low_confidence": confidence < 0.60,
            "description": treatment["description"],
            "severity": treatment["severity"],
            "treatment_steps": treatment["steps"],
        }


disease_service = DiseaseService()
