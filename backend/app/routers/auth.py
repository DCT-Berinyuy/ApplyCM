from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.user import User, UserCreate
from app.services.auth_service import AuthService
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    return AuthService.create_user(db=db, user_in=user_in)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(db=db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout():
    """
    Stateless JWT Logout endpoint.
    In a stateless JWT architecture, the server does not track active tokens.
    Calling logout signals the frontend to clear its stored token.
    """
    return {"message": "Successfully logged out"}

@router.get("/me", response_model=User)
def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Protected test route.
    Requires a valid JWT Bearer token in the Authorization header.
    Returns the current authenticated user profile.
    """
    return current_user
