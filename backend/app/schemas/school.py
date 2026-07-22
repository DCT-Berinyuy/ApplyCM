from pydantic import BaseModel
from typing import Optional

class SchoolBase(BaseModel):
    name: str
    location: str
    description: Optional[str] = None
    logo_url: Optional[str] = None

class SchoolCreate(SchoolBase):
    pass

class SchoolUpdate(BaseModel):
    name: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None

class School(SchoolBase):
    id: int

    class Config:
        from_attributes = True
