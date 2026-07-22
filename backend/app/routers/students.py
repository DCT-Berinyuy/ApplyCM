from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.student_profile import StudentProfile, StudentProfileCreate, StudentProfileUpdate
from app.models.user import User
from app.services.student_service import StudentService

router = APIRouter(prefix="/students", tags=["students"])

@router.get("/me", response_model=StudentProfile)
def get_my_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # TODO: Call StudentService.get_profile_by_user_id
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.post("/", response_model=StudentProfile, status_code=status.HTTP_201_CREATED)
def create_profile(profile_in: StudentProfileCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # TODO: Call StudentService.create_profile
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.put("/me", response_model=StudentProfile)
def update_profile(profile_in: StudentProfileUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # TODO: Call StudentService.update_profile
    raise HTTPException(status_code=501, detail="Not Implemented")
