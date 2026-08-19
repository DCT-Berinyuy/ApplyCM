from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class DocumentBase(BaseModel):
    student_id: UUID
    file_url: str
    doc_type: str

class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    file_url: Optional[str] = None
    doc_type: Optional[str] = None

class Document(DocumentBase):
    id: UUID
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

