from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserBase(BaseModel):
    email: str
    is_active: Optional[bool] = True
    role: Optional[str] = "student"

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: UUID
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

