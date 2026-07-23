from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    nationality = Column(String, default="Cameroonian")
    high_school = Column(String, nullable=True)

    # TODO: Add relationships to applications, favorites, documents, etc.
    # user = relationship("User", back_populates="profile")
    # applications = relationship("Application", back_populates="student_profile")
    # favorites = relationship("Favorite", back_populates="student_profile")
    # documents = relationship("Document", back_populates="student_profile")
