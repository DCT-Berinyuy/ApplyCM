from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.user import User, UserCreate
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    # TODO: Call AuthService.create_user
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.post("/login")
def login(db: Session = Depends(get_db)):
    # TODO: Call AuthService.authenticate_user and return access token
    raise HTTPException(status_code=501, detail="Not Implemented")
