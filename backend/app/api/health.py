from fastapi import APIRouter
from app.database.sqlite import get_db

router = APIRouter(tags=["Health"])


@router.get("/api/health")
def health():
    conn = get_db()
    conn.execute("SELECT 1").fetchone()
    conn.close()
    return {"status": "ok", "database": "sqlite"}
