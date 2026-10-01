from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.schemas.program import Program

class SchoolBase(BaseModel):
    name: str
    location: Optional[str] = None
    description: Optional[str] = None
    website_url: Optional[str] = None
    logo_url: Optional[str] = None
    contact_email: Optional[str] = None
    application_deadline: Optional[str] = None
    rolling_admission: Optional[bool] = False
    institution_type: Optional[str] = None
    city: Optional[str] = None
    data_source_url: Optional[str] = None
    last_verified_at: Optional[datetime] = None

class SchoolCreate(SchoolBase):
    pass

class SchoolUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    website_url: Optional[str] = None
    logo_url: Optional[str] = None
    contact_email: Optional[str] = None
    application_deadline: Optional[str] = None
    rolling_admission: Optional[bool] = None
    institution_type: Optional[str] = None
    city: Optional[str] = None
    data_source_url: Optional[str] = None
    last_verified_at: Optional[datetime] = None


class School(SchoolBase):
    id: UUID
    created_at: Optional[datetime] = None
    programs: Optional[List[Program]] = []

    class Config:
        from_attributes = True