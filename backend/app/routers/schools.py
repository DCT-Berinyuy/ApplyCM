from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.dependencies import get_db
from app.schemas.school import School, SchoolCreate
from app.schemas.program import Program
from app.services.school_service import SchoolService
from app.services.program_service import ProgramService

router = APIRouter(prefix="/schools", tags=["schools"])

@router.get("", response_model=List[School])
@router.get("/", response_model=List[School], include_in_schema=False)
def list_schools(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = Query(None, description="Search keyword for name, location, field of study, description"),
    q: Optional[str] = Query(None, description="Alias for search"),
    institution_type: Optional[str] = Query(None, description="Filter by institution type (e.g. public, ipes, iup)"),
    city: Optional[str] = Query(None, description="Filter by city or region"),
    field_of_study: Optional[str] = Query(None, description="Filter by program field of study"),
    degree_type: Optional[str] = Query(None, description="Filter by degree type"),
    min_tuition: Optional[int] = Query(None, description="Minimum tuition fee in FCFA"),
    max_tuition: Optional[int] = Query(None, description="Maximum tuition fee in FCFA"),
    language_of_instruction: Optional[str] = Query(None, description="Language of instruction"),
    delivery_mode: Optional[str] = Query(None, description="Delivery mode (e.g. On-Campus, Hybrid)"),
    db: Session = Depends(get_db)
):
    query_term = search or q
    return SchoolService.list_schools(
        db,
        skip=skip,
        limit=limit,
        search=query_term,
        institution_type=institution_type,
        city=city,
        field_of_study=field_of_study,
        degree_type=degree_type,
        min_tuition=min_tuition,
        max_tuition=max_tuition,
        language_of_instruction=language_of_instruction,
        delivery_mode=delivery_mode,
    )

@router.get("/{school_id}", response_model=School)
def get_school(school_id: UUID, db: Session = Depends(get_db)):
    school = SchoolService.get_school(db, school_id=school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school

@router.get("/{school_id}/programs", response_model=List[Program])
def get_school_programs(school_id: UUID, db: Session = Depends(get_db)):
    school = SchoolService.get_school(db, school_id=school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return ProgramService.list_programs(db, school_id=school_id)

@router.post("/", response_model=School, status_code=status.HTTP_201_CREATED)
def create_school(school_in: SchoolCreate, db: Session = Depends(get_db)):
    return SchoolService.create_school(db, school_in=school_in)