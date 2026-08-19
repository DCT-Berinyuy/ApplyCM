from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class StudentProfileBase(BaseModel):
    full_name: str
    phone: Optional[str] = None
    education_summary: Optional[str] = None
    writing_sample: Optional[str] = None

class StudentProfileCreate(StudentProfileBase):
    user_id: UUID

class StudentProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    education_summary: Optional[str] = None
    writing_sample: Optional[str] = None

class StudentProfile(StudentProfileBase):
    id: UUID
    user_id: UUID
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

