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
    # TODO: Call ApplicationService.create_application
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.post("/batch", response_model=List[Application], status_code=status.HTTP_201_CREATED)
def apply_to_multiple_programs(batch_in: BatchApplicationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # TODO: Call ApplicationService.apply_to_multiple_programs
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.get("/", response_model=List[Application])
def list_my_applications(student_profile_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # TODO: Call ApplicationService.list_applications_by_student
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.get("/{application_id}", response_model=Application)
def get_application(application_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # TODO: Call ApplicationService.get_application
    raise HTTPException(status_code=501, detail="Not Implemented")
