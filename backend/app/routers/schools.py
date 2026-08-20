from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db
from app.schemas.school import School
from app.services.school_service import SchoolService

router = APIRouter(prefix="/schools", tags=["schools"])

@router.get("/", response_model=List[School])
def list_schools(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return SchoolService.list_schools(db, skip=skip, limit=limit)

@router.get("/{school_id}", response_model=School)
def get_school(school_id: UUID, db: Session = Depends(get_db)):
    school = SchoolService.get_school(db, school_id=school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school

