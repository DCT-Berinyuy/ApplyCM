from uuid import UUID
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
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


    @staticmethod
    def save_section(db: Session, user_id: UUID, section: str, section_in: BaseModel) -> StudentProfile:
        """Write one application-profile wizard section for the given account.

        The profile row is created on first save, so the wizard sections can be
        filled in any order. Ownership comes from ``user_id`` (the token), never
        from the request body.
        """
        values = section_in.model_dump()
        if section == "profile":
            values["full_name"] = f"{values['first_name']} {values['last_name']}"

        profile = StudentService.get_profile_by_user_id(db, user_id)
        if profile is None:
            profile = StudentProfile(user_id=user_id, **values)
            db.add(profile)
            try:
                db.commit()
            except IntegrityError:
                # A concurrent first save for this account won the insert on
                # the unique user_id; fall through and update that row instead.
                db.rollback()
                profile = StudentService.get_profile_by_user_id(db, user_id)
                if profile is None:
                    raise
            else:
                db.refresh(profile)
                return profile

        for key, val in values.items():
            setattr(profile, key, val)
        db.commit()
        db.refresh(profile)
        return profile
