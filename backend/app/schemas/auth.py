from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    mobile_number: str = Field(min_length=8, max_length=20)
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str
    state: str = ""
    district: str = ""
    village: str = ""

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, value, info):
        if value != info.data.get("password"):
            raise ValueError("Passwords do not match")
        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    mobile_number: str
    state: str
    district: str
    village: str
    preferred_language: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
