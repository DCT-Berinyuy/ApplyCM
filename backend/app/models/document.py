import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    student_id = Column(UUID(as_uuid=True), ForeignKey("student_profiles.id", ondelete="CASCADE"), nullable=False, index=True)
    file_url = Column(String, nullable=False)
    doc_type = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    @property
    def student_profile_id(self):
        return self.student_id

    @student_profile_id.setter
    def student_profile_id(self, value):
        self.student_id = value

    @property
    def document_type(self):
        return self.doc_type

    @document_type.setter
    def document_type(self, value):
        self.doc_type = value

