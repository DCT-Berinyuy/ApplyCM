from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.core.security import get_password_hash, verify_password

class AuthService:
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_user(db: Session, user_in: UserCreate) -> User:
        # 1. Check if user with this email already exists
        existing_user = db.query(User).filter(User.email == user_in.email).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # 2. Hash the plain password using security utility
        hashed_password = get_password_hash(user_in.password)

        # 3. Instantiate SQLAlchemy User model
        db_user = User(
            email=user_in.email,
            hashed_password=hashed_password,
            role=user_in.role if user_in.role else "student",
            is_active=True
        )

        # 4. Save to database transactionally
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
