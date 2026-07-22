from pydantic import BaseModel
from typing import Optional

class DocumentBase(BaseModel):
    student_profile_id: int
    name: str
    document_type: str
    file_url: str

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    name: Optional[str] = None
    document_type: Optional[str] = None
    file_url: Optional[str] = None

class Document(DocumentBase):
    id: int

    class Config:
        from_attributes = True
