from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_current_user
from app.schemas.application import Application, ApplicationCreate, BatchApplicationCreate
from app.models.user import User
from app.services.application_service import ApplicationService

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("/", response_model=Application, status_code=status.HTTP_201_CREATED)
def apply_to_program(application_in: ApplicationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ApplicationService.create_application(db, application_in)

@router.post("/batch", response_model=List[Application], status_code=status.HTTP_201_CREATED)
def apply_to_multiple_programs(batch_in: BatchApplicationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ApplicationService.apply_to_multiple_programs(db, batch_in)

@router.get("/", response_model=List[Application])
def list_my_applications(student_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ApplicationService.list_applications_by_student(db, student_id=student_id)

@router.get("/{application_id}", response_model=Application)
def get_application(application_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    app_item = ApplicationService.get_application(db, application_id=application_id)
    if not app_item:
        raise HTTPException(status_code=404, detail="Application not found")
    return app_item

