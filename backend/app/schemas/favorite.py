from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class FavoriteBase(BaseModel):
    student_id: UUID
    school_id: UUID

class FavoriteCreate(FavoriteBase):
    pass

class Favorite(FavoriteBase):
    id: UUID
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

