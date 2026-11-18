import json
from fastapi import APIRouter, HTTPException, Depends
from app.database.sqlite import get_db
from app.schemas.prediction import CropInput, CropResponse
from app.services.crop_service import crop_service
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/api/crop", tags=["Crop Recommendation"])


@router.post("/recommend", response_model=CropResponse)
def recommend(payload: CropInput, user: dict = Depends(get_current_user)):
    values = {
        "N": payload.nitrogen,
        "P": payload.phosphorus,
        "K": payload.potassium,
        "temperature": payload.temperature,
        "humidity": payload.humidity,
        "ph": payload.ph,
        "rainfall": payload.rainfall,
    }
    try:
        result = crop_service.predict(values)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))

    conn = get_db()
    conn.execute("""INSERT INTO crop_recommendations
        (user_id, nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall,
         recommended_crop, alternatives, model_used)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
        user["id"], payload.nitrogen, payload.phosphorus, payload.potassium,
        payload.temperature, payload.humidity, payload.ph, payload.rainfall,
        result["recommended_crop"], json.dumps(result["alternatives"]), result["model_used"]
    ))
    conn.commit()
    conn.close()
    return result


@router.get("/history")
def history(limit: int = 25, user=Depends(get_current_user)):
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM crop_recommendations WHERE user_id = ? ORDER BY id DESC LIMIT ?",
        (user["id"], min(limit, 100))
    ).fetchall()
    conn.close()
    return [dict(row) | {"alternatives": json.loads(row["alternatives"] or "[]")} for row in rows]


@router.get("/supported-crops")
def supported_crops():
    return {"crops": ["rice", "maize", "chickpea", "kidneybeans", "pigeonpeas", "mothbeans", "mungbean", "blackgram", "lentil", "pomegranate", "banana", "mango", "grapes", "watermelon", "muskmelon", "apple", "orange", "papaya", "coconut", "cotton", "jute", "coffee"]}
