from uuid import UUID
from typing import List
from sqlalchemy.orm import Session
from app.schemas.application import ApplicationCreate, BatchApplicationCreate
from app.models.application import Application

class ApplicationService:
    @staticmethod
    def get_application(db: Session, application_id: UUID) -> Application:
        return db.query(Application).filter(Application.id == application_id).first()

    @staticmethod
    def list_applications_by_student(db: Session, student_id: UUID) -> List[Application]:
        return db.query(Application).filter(Application.student_id == student_id).all()

    @staticmethod
    def create_application(db: Session, application_in: ApplicationCreate) -> Application:
        db_app = Application(**application_in.model_dump())
        db.add(db_app)
        db.commit()
        db.refresh(db_app)
        return db_app

    @staticmethod
    def apply_to_multiple_programs(db: Session, batch_in: BatchApplicationCreate) -> List[Application]:
        applications = []
        for pid in batch_in.program_ids:
            app = Application(student_id=batch_in.student_id, program_id=pid, status="submitted")
            db.add(app)
            applications.append(app)
        db.commit()
        for app in applications:
            db.refresh(app)
        return applications

