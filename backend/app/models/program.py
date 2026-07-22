from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)
    school_id = Column(Integer, ForeignKey("schools.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    duration_years = Column(Integer, default=3)

    # TODO: Add relationships to school, applications, etc.
    # school = relationship("School", back_populates="programs")
    # applications = relationship("Application", back_populates="program")
