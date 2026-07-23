from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ApplicationBase(BaseModel):
    student_profile_id: int
    program_id: int
    status: Optional[str] = "pending"

class ApplicationCreate(ApplicationBase):
    pass

class BatchApplicationCreate(BaseModel):
    student_profile_id: int
    program_ids: List[int]

class ApplicationUpdate(BaseModel):
    status: Optional[str] = None

class Application(ApplicationBase):
    id: int
    submitted_at: datetime

    class Config:
        from_attributes = True
