from fastapi import APIRouter, Depends, HTTPException, status
from app.database.sqlite import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.core.dependencies import get_current_user
from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


def public_user(row: dict) -> UserResponse:
    keys = ["id", "full_name", "email", "mobile_number", "state", "district", "village", "preferred_language", "role"]
    data = {}
    for key in keys:
        val = row.get(key)
        if val is None:
            val = "" if key in ("mobile_number", "state", "district", "village") else ("en" if key == "preferred_language" else ("farmer" if key == "role" else ""))
        data[key] = val
    return UserResponse(**data)


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(payload: RegisterRequest):
    conn = get_db()
    if conn.execute("SELECT id FROM users WHERE LOWER(email) = ?", (payload.email.lower().strip(),)).fetchone():
        conn.close()
        raise HTTPException(status_code=409, detail="An account with this email already exists")
    cursor = conn.execute("""INSERT INTO users
        (full_name, email, mobile_number, password_hash, state, district, village)
        VALUES (?, ?, ?, ?, ?, ?, ?)""", (
        payload.full_name.strip(), payload.email.lower().strip(), payload.mobile_number or "",
        hash_password(payload.password), payload.state or "", payload.district or "", payload.village or ""
    ))
    conn.commit()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (cursor.lastrowid,)).fetchone()
    conn.close()
    user = dict(row)
    return TokenResponse(access_token=create_access_token(user["id"]), user=public_user(user))


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE LOWER(email) = ?", (payload.email.lower().strip(),)).fetchone()
    conn.close()
    if not row or not verify_password(payload.password, row["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    user = dict(row)
    return TokenResponse(access_token=create_access_token(user["id"]), user=public_user(user))


@router.get("/me", response_model=UserResponse)
def me(user: dict = Depends(get_current_user)):
    return public_user(user)
