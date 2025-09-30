from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional
from datetime import datetime
import re
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    staff = "staff"

class UserBase(BaseModel):
    username: str = Field(..., min_length=6, max_length=15, pattern=r"^[a-z0-9]+$")
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=20)
    role: UserRole

    @validator('password')
    def validate_password(cls, v):
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[0-9]", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[!@]", v):
            raise ValueError("Password must contain at least one special character: ! or @")
        if re.search(r"[^a-zA-Z0-9!@]", v):
            raise ValueError("Password contains invalid characters")
        return v

class User(UserBase):
    id: int
    role: UserRole
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=6, max_length=15, pattern=r"^[a-z0-9]+$")
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None