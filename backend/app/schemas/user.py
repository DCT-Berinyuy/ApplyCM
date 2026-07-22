from pydantic import BaseModel
from typing import Optional

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
    id: int

    class Config:
        from_attributes = True
