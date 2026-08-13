from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base



class User(Base):
    __tablename__ = "users"
    
    # PostgreSQL equivalent:
    # CREATE TABLE users (
    #     id SERIAL PRIMARY KEY,
    #     email VARCHAR UNIQUE NOT NULL,
    #     hashed_password VARCHAR NOT NULL,
    #     is_active BOOLEAN DEFAULT TRUE,
    #     role VARCHAR DEFAULT 'student'
    # );

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="student") # e.g. student, admin, school_admin

    # TODO: Define relationship to StudentProfile or other entities
    # profile = relationship("StudentProfile", back_populates="user", uselist=False)
