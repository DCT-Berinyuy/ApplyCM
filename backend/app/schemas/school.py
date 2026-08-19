from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class SchoolBase(BaseModel):
    name: str
    city: Optional[str] = None
    arrondissement: Optional[str] = None
    description: Optional[str] = None

class SchoolCreate(SchoolBase):
    pass

class SchoolUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    arrondissement: Optional[str] = None
    description: Optional[str] = None

class School(SchoolBase):
    id: UUID
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

