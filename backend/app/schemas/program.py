from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from uuid import UUID
from datetime import datetime

class ProgramBase(BaseModel):
    field_of_study: str
    tuition: Optional[Decimal] = None
    admission_requirements: Optional[str] = None

class ProgramCreate(ProgramBase):
    school_id: UUID

class ProgramUpdate(BaseModel):
    field_of_study: Optional[str] = None
    tuition: Optional[Decimal] = None
    admission_requirements: Optional[str] = None

class Program(ProgramBase):
    id: UUID
    school_id: UUID
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

