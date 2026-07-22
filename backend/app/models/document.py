from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    student_profile_id = Column(Integer, ForeignKey("student_profiles.id"), nullable=False)
    name = Column(String, nullable=False) # e.g. Transcripts, Recommendation Letter
    document_type = Column(String, nullable=False) # e.g. pdf, image
    file_url = Column(String, nullable=False)

    # TODO: Add relationships to student_profile
    # student_profile = relationship("StudentProfile", back_populates="documents")
