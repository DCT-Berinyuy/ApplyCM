from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    student_profile_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)
    status = Column(String, default="pending") # pending, submitted, under_review, accepted, rejected
    submitted_at = Column(DateTime, default=datetime.utcnow)

    # TODO: Add relationships to student_profile, program, etc.
    # student_profile = relationship("StudentProfile", back_populates="applications")
    # program = relationship("Program", back_populates="applications")
