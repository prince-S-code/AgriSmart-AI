from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.database.sqlite import get_db
from app.core.dependencies import get_current_user
from app.services.disease_service import disease_service

router = APIRouter(prefix="/api/disease", tags=["Disease Detection"])
UPLOAD_DIR = Path(__file__).resolve().parents[3] / "uploads" / "disease"


@router.post("/predict")
async def predict(image: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    if image.content_type not in {"image/jpeg", "image/png"}:
        raise HTTPException(status_code=400, detail="Only JPG, JPEG and PNG images are allowed")
    content = await image.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image exceeds the 5 MB limit")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    suffix = ".png" if image.content_type == "image/png" else ".jpg"
    image_name = f"{uuid4().hex}{suffix}"
    image_path = UPLOAD_DIR / image_name
    image_path.write_bytes(content)

    try:
        result = disease_service.predict(image_path)
    except Exception as exc:
        image_path.unlink(missing_ok=True)
        raise HTTPException(status_code=503, detail=f"Disease inference unavailable: {exc}")

    conn = get_db()
    conn.execute("""INSERT INTO disease_predictions
        (user_id, image_name, crop_name, predicted_disease, confidence, model_used)
        VALUES (?, ?, ?, ?, ?, ?)""", (
        current_user["id"], str(image_path), result["crop_name"],
        result["predicted_disease"], result["confidence"], result["model_used"]
    ))
    conn.commit()
    conn.close()
    return result


@router.get("/history")
def history(limit: int = 25, current_user: dict = Depends(get_current_user)):
    conn = get_db()
    rows = conn.execute("SELECT * FROM disease_predictions WHERE user_id = ? ORDER BY id DESC LIMIT ?", (current_user['id'], min(limit, 100))).fetchall()
    conn.close()
    return [dict(row) for row in rows]


@router.get("/supported-classes")
def supported_classes():
    if not disease_service.is_available():
        return {"available": False, "message": "Disease model artifact is unavailable", "supported_classes": []}
    if disease_service.metadata is None:
        import json
        metadata_path = Path(__file__).resolve().parents[2] / "trained_models" / "disease" / "metadata.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    else:
        metadata = disease_service.metadata
    return {"available": True, "supported_classes": metadata["class_names"]}
