from uuid import UUID
from sqlalchemy.orm import Session
from app.schemas.student_profile import StudentProfileCreate, StudentProfileUpdate
from app.models.student_profile import StudentProfile

class StudentService:
    @staticmethod
    def get_profile(db: Session, student_id: UUID) -> StudentProfile:
        return db.query(StudentProfile).filter(StudentProfile.id == student_id).first()

    @staticmethod
    def get_profile_by_user_id(db: Session, user_id: UUID) -> StudentProfile:
        return db.query(StudentProfile).filter(StudentProfile.user_id == user_id).first()

    @staticmethod
    def create_profile(db: Session, profile_in: StudentProfileCreate) -> StudentProfile:
        db_profile = StudentProfile(**profile_in.model_dump())
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile

    @staticmethod
    def update_profile(db: Session, student_id: UUID, profile_in: StudentProfileUpdate) -> StudentProfile:
        db_profile = StudentService.get_profile(db, student_id)
        if db_profile:
            for key, val in profile_in.model_dump(exclude_unset=True).items():
                setattr(db_profile, key, val)
            db.commit()
            db.refresh(db_profile)
        return db_profile

