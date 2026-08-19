from uuid import UUID
from typing import List
from sqlalchemy.orm import Session
from app.schemas.school import SchoolCreate, SchoolUpdate
from app.models.school import School

class SchoolService:
    @staticmethod
    def get_school(db: Session, school_id: UUID) -> School:
        return db.query(School).filter(School.id == school_id).first()

    @staticmethod
    def list_schools(db: Session, skip: int = 0, limit: int = 100) -> List[School]:
        return db.query(School).offset(skip).limit(limit).all()

    @staticmethod
    def create_school(db: Session, school_in: SchoolCreate) -> School:
        db_school = School(**school_in.model_dump())
        db.add(db_school)
        db.commit()
        db.refresh(db_school)
        return db_school

