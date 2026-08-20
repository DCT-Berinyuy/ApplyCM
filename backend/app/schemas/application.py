from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class ApplicationBase(BaseModel):
    student_id: UUID
    program_id: UUID
    status: Optional[str] = "submitted"

class ApplicationCreate(ApplicationBase):
    pass

class BatchApplicationCreate(BaseModel):
    student_id: UUID
    program_ids: List[UUID]

class ApplicationUpdate(BaseModel):
    status: Optional[str] = None

class Application(ApplicationBase):
    id: UUID
    submitted_at: datetime

    class Config:
        from_attributes = True

