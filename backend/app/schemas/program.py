from pydantic import BaseModel
from typing import Optional

class ProgramBase(BaseModel):
    name: str
    description: Optional[str] = None
    duration_years: Optional[int] = 3

class ProgramCreate(ProgramBase):
    school_id: int

class ProgramUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    duration_years: Optional[int] = None

class Program(ProgramBase):
    id: int
    school_id: int

    class Config:
        from_attributes = True
