from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parents[2] / "trained_models" / "disease" / "AgriSmart_AI_YOLOv8.pt"


class YoloService:
    def __init__(self):
        self.model = None

    def is_available(self) -> bool:
        return MODEL_PATH.is_file()

    def _load(self):
        if self.model is not None:
            return
        if not self.is_available():
            raise RuntimeError(f"YOLO model artifact is missing: {MODEL_PATH.name}")
        from ultralytics import YOLO

        self.model = YOLO(str(MODEL_PATH))

    def predict(self, image_path: Path):
        self._load()
        result = self.model.predict(source=str(image_path), device="cpu", verbose=False)[0]
        names = result.names

        if result.probs is not None:
            class_index = int(result.probs.top1)
            confidence = float(result.probs.top1conf)
            predictions = [{
                "class_name": names[class_index],
                "confidence": round(confidence, 4),
            }]
        else:
            predictions = []
            if result.boxes is not None:
                for box in result.boxes:
                    class_index = int(box.cls.item())
                    predictions.append({
                        "class_name": names[class_index],
                        "confidence": round(float(box.conf.item()), 4),
                    })
            predictions.sort(key=lambda prediction: prediction["confidence"], reverse=True)

        best = predictions[0] if predictions else None
        return {
            "model": "YOLOv8",
            "predicted_disease": best["class_name"] if best else "No disease detected",
            "confidence": best["confidence"] if best else 0.0,
            "test_accuracy": None,
            "detections": predictions,
        }


yolo_service = YoloService()
