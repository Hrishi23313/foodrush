from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.models.enums import UserRole


class UserRegister(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(default=None, pattern=r"^\+?[0-9]{10,15}$")
    password: str = Field(min_length=8, max_length=64)
    role: Literal["customer", "owner"] = "customer"

    @field_validator("full_name")
    @classmethod
    def clean_name(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Full name must be at least 2 characters")
        return value

    @field_validator("email")
    @classmethod
    def lowercase_email(cls, value: str) -> str:
        return value.lower()

    @field_validator("password")
    @classmethod
    def check_password_strength(cls, value: str) -> str:
        if not any(ch.isalpha() for ch in value):
            raise ValueError("Password must contain at least one letter")
        if not any(ch.isdigit() for ch in value):
            raise ValueError("Password must contain at least one digit")
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password is too long")
        return value


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def lowercase_email(cls, value: str) -> str:
        return value.lower()


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    role: UserRole
    is_active: bool
    created_at: datetime