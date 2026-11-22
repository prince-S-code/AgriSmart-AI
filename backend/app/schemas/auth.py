from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    confirm_password: str | None = None
    mobile_number: str | None = ""
    state: str | None = ""
    district: str | None = ""
    village: str | None = ""

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, value, info):
        if value is not None and value != info.data.get("password"):
            raise ValueError("Passwords do not match")
        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    mobile_number: str | None = ""
    state: str | None = ""
    district: str | None = ""
    village: str | None = ""
    preferred_language: str = "en"
    role: str = "farmer"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
