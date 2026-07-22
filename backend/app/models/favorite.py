from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    student_profile_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)

    # TODO: Add relationships to student_profile, school, etc.
    # student_profile = relationship("StudentProfile", back_populates="favorites")
    # school = relationship("School")
