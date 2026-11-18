from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.database.sqlite import get_db

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/stats")
def stats(user: dict = Depends(get_current_user)):
    conn = get_db()
    crop_count = conn.execute("SELECT COUNT(*) FROM crop_recommendations WHERE user_id = ?", (user["id"],)).fetchone()[0]
    disease_count = conn.execute("SELECT COUNT(*) FROM disease_predictions WHERE user_id = ?", (user["id"],)).fetchone()[0]
    recent_crops = conn.execute("SELECT recommended_crop, created_at FROM crop_recommendations WHERE user_id = ? ORDER BY id DESC LIMIT 3", (user["id"],)).fetchall()
    conn.close()
    return {"crop_recommendations": crop_count, "disease_scans": disease_count, "recent_crops": [dict(row) for row in recent_crops]}
