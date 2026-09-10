"""Student profile model.

The applicant-facing extension of a :class:`~app.models.user.User` account.
The relationship is strictly one-to-one: enforced at the database level by a
unique constraint on ``user_id`` and at the ORM level by ``uselist=False`` on
the reverse side.

This module is intentionally DDL-neutral with respect to the live schema —
every column and constraint mirrors migration ``0dd12cfb019b`` exactly, so no
new Alembic revision is required. Constraint names are pinned so that
``alembic revision --autogenerate`` does not propose a spurious drop/recreate.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    # Imported for typing only; the runtime link is resolved by SQLAlchemy from
    # the string target, which keeps User <-> StudentProfile free of a circular
    # import at module load time.
    from app.models.user import User


class StudentProfile(Base):
    """A student's application profile. Exactly one per :class:`User`."""

    __tablename__ = "student_profiles"
    __table_args__ = (
        # Named to match the constraint created by migration 0dd12cfb019b.
        UniqueConstraint("user_id", name="uq_student_profiles_user"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str | None] = mapped_column(String, nullable=True)
    education_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    writing_sample: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Owning account. `passive_deletes` defers cascade to the database, which
    # already declares ON DELETE CASCADE on the foreign key.
    user: Mapped[User] = relationship(
        "User",
        back_populates="student_profile",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return f"<StudentProfile id={self.id!s} user_id={self.user_id!s}>"
