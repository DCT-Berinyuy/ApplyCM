from pydantic import BaseModel

class FavoriteBase(BaseModel):
    student_profile_id: int
    school_id: int

class FavoriteCreate(FavoriteBase):
    pass

class Favorite(FavoriteBase):
    id: int

    class Config:
        from_attributes = True
