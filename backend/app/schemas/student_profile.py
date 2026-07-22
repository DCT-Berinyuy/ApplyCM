from pydantic import BaseModel
from typing import Optional

class StudentProfileBase(BaseModel):
    first_name: str
    last_name: str
    phone: Optional[str] = None
    nationality: Optional[str] = "Cameroonian"
    high_school: Optional[str] = None

class StudentProfileCreate(StudentProfileBase):
    user_id: int

class StudentProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    nationality: Optional[str] = None
    high_school: Optional[str] = None

class StudentProfile(StudentProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
