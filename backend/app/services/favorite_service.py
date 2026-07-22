from sqlalchemy.orm import Session
from typing import List
from app.schemas.favorite import FavoriteCreate
from app.models.favorite import Favorite

class FavoriteService:
    @staticmethod
    def get_favorites_by_student(db: Session, student_profile_id: int) -> List[Favorite]:
        # TODO: Implement list student favorites logic
        return []

    @staticmethod
    def add_favorite(db: Session, favorite_in: FavoriteCreate) -> Favorite:
        # TODO: Implement add favorite school logic
        return None

    @staticmethod
    def remove_favorite(db: Session, student_profile_id: int, school_id: int) -> bool:
        # TODO: Implement remove favorite school logic
        return False
