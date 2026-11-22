import logging
import os
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from app.database.sqlite import get_db
from app.core.dependencies import get_current_user
from app.core.config import settings
from app.services.disease_service import disease_service
from app.services.yolo_service import yolo_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/disease", tags=["Disease Detection"])
UPLOAD_DIR = Path(settings.upload_dir) / "disease"
ENABLE_YOLO = os.getenv("ENABLE_YOLO", "true").lower() in {"true", "1", "yes"}


@router.post("/predict")
async def predict(image: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    if image.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(status_code=400, detail="Only JPG, JPEG and PNG images are allowed")
    content = await image.read()
    max_upload_bytes = settings.max_upload_mb * 1024 * 1024
    if len(content) > max_upload_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"Image exceeds the {settings.max_upload_mb} MB limit",
        )
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded image is empty")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    suffix = ".png" if image.content_type == "image/png" else ".jpg"
    image_name = f"{uuid4().hex}{suffix}"
    image_path = UPLOAD_DIR / image_name
    image_path.write_bytes(content)

    try:
        try:
            result = disease_service.predict(image_path)
        except Exception as exc:
            logger.exception("CNN disease inference failed")
            raise HTTPException(
                status_code=503,
                detail=f"CNN inference unavailable: {exc}",
            ) from exc

        model_results = [{
            "model": "MobileNetV2 CNN",
            "predicted_disease": result["predicted_disease"],
            "confidence": result["confidence"],
            "test_accuracy": result["test_accuracy"],
            "detections": [],
        }]
        if ENABLE_YOLO:
            try:
                model_results.append(yolo_service.predict(image_path))
            except Exception:
                logger.exception("YOLO inference failed; returning the CNN prediction")
                model_results.append({
                    "model": "YOLOv8",
                    "predicted_disease": "Prediction unavailable",
                    "confidence": 0.0,
                    "test_accuracy": None,
                    "detections": [],
                    "available": False,
                })
        else:
            model_results.append({
                "model": "YOLOv8",
                "predicted_disease": "Not enabled on this deployment",
                "confidence": 0.0,
                "test_accuracy": None,
                "detections": [],
                "available": False,
            })

        conn = get_db()
        try:
            conn.execute(
                """INSERT INTO disease_predictions
                (user_id, image_name, crop_name, predicted_disease, confidence, model_used)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    current_user["id"], str(image_path), result["crop_name"],
                    result["predicted_disease"], result["confidence"],
                    "MobileNetV2 CNN" + (" + YOLOv8" if ENABLE_YOLO else ""),
                ),
            )
            conn.commit()
        finally:
            conn.close()

        result["model_results"] = model_results
        return result
    finally:
        image_path.unlink(missing_ok=True)

@router.get("/history")
def history(limit: int = 25, current_user: dict = Depends(get_current_user)):
    conn = get_db()
    try:
        rows = conn.execute(
            "SELECT * FROM disease_predictions WHERE user_id = ? ORDER BY id DESC LIMIT ?",
            (current_user["id"], min(limit, 100)),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


@router.get("/supported-classes")
def supported_classes():
    if not disease_service.is_available():
        return {
            "available": False,
            "message": "Disease model artifact is unavailable",
            "supported_classes": [],
        }
    if disease_service.metadata is None:
        import json

        metadata_path = Path(__file__).resolve().parents[2] / "trained_models" / "disease" / "metadata.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    else:
        metadata = disease_service.metadata
    return {"available": True, "supported_classes": metadata["class_names"]}
