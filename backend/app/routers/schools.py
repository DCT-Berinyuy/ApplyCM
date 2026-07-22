from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from app.schemas.school import School
from app.services.school_service import SchoolService

router = APIRouter(prefix="/schools", tags=["schools"])

@router.get("/", response_model=List[School])
def list_schools(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # TODO: Call SchoolService.list_schools
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.get("/{school_id}", response_model=School)
def get_school(school_id: int, db: Session = Depends(get_db)):
    # TODO: Call SchoolService.get_school
    raise HTTPException(status_code=501, detail="Not Implemented")
