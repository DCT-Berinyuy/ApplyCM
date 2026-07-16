from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.dependencies import get_db, get_current_user
from app.schemas.favorite import Favorite, FavoriteCreate
from app.models.user import User
from app.services.favorite_service import FavoriteService

router = APIRouter(prefix="/favorites", tags=["favorites"])

@router.get("/", response_model=List[Favorite])
def list_my_favorites(student_profile_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # TODO: Call FavoriteService.get_favorites_by_student
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.post("/", response_model=Favorite, status_code=status.HTTP_201_CREATED)
def add_favorite(favorite_in: FavoriteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # TODO: Call FavoriteService.add_favorite
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.delete("/{school_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(student_profile_id: int, school_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # TODO: Call FavoriteService.remove_favorite
    raise HTTPException(status_code=501, detail="Not Implemented")
