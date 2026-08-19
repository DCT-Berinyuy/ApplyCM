from uuid import UUID
from typing import List
from sqlalchemy.orm import Session
from app.schemas.favorite import FavoriteCreate
from app.models.favorite import Favorite

class FavoriteService:
    @staticmethod
    def get_favorites_by_student(db: Session, student_id: UUID) -> List[Favorite]:
        return db.query(Favorite).filter(Favorite.student_id == student_id).all()

    @staticmethod
    def add_favorite(db: Session, favorite_in: FavoriteCreate) -> Favorite:
        db_fav = Favorite(**favorite_in.model_dump())
        db.add(db_fav)
        db.commit()
        db.refresh(db_fav)
        return db_fav

    @staticmethod
    def remove_favorite(db: Session, student_id: UUID, school_id: UUID) -> bool:
        fav = db.query(Favorite).filter(
            Favorite.student_id == student_id,
            Favorite.school_id == school_id
        ).first()
        if fav:
            db.delete(fav)
            db.commit()
            return True
        return False

