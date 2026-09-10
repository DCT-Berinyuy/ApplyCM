"""Persistence logic for student profiles.

Ownership is always passed in explicitly by the caller, which has already
resolved it from the access token. Nothing here trusts a client-supplied
``user_id``.
"""

from __future__ import annotations

import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.student_profile import StudentProfile
from app.schemas.student_profile import StudentProfileCreate, StudentProfileUpdate


class StudentService:
    """Data-access helpers for the ``student_profiles`` table."""

    @staticmethod
    def get_profile(db: Session, student_id: uuid.UUID) -> StudentProfile | None:
        """Return the profile with this primary key, or ``None``."""
        return db.execute(
            select(StudentProfile).where(StudentProfile.id == student_id)
        ).scalar_one_or_none()

    @staticmethod
    def get_profile_by_user_id(
        db: Session, user_id: uuid.UUID
    ) -> StudentProfile | None:
        """Return the profile owned by this account, or ``None``."""
        return db.execute(
            select(StudentProfile).where(StudentProfile.user_id == user_id)
        ).scalar_one_or_none()

    @staticmethod
    def create_profile(
        db: Session, *, user_id: uuid.UUID, profile_in: StudentProfileCreate
    ) -> StudentProfile:
        """Insert a profile owned by ``user_id``.

        Raises :class:`sqlalchemy.exc.IntegrityError` if the account already
        has one, since ``uq_student_profiles_user`` forbids a second row.
        """
        profile = StudentProfile(user_id=user_id, **profile_in.model_dump())
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def apply_update(
        db: Session,
        *,
        profile: StudentProfile,
        profile_in: StudentProfileUpdate | StudentProfileCreate,
        partial: bool = True,
    ) -> StudentProfile:
        """Write ``profile_in`` onto an already-loaded ``profile``.

        With ``partial=True`` only fields the client actually sent are copied,
        so an omitted key leaves the stored value untouched.
        """
        payload = profile_in.model_dump(exclude_unset=partial)
        for field, value in payload.items():
            setattr(profile, field, value)
        db.commit()
        db.refresh(profile)
        return profile

    @staticmethod
    def upsert_own_profile(
        db: Session, *, user_id: uuid.UUID, profile_in: StudentProfileCreate
    ) -> tuple[StudentProfile, bool]:
        """Create the account's profile, or replace it if one already exists.

        Returns ``(profile, created)``. Two concurrent first-time writes both
        see an empty row set and both attempt an insert; the unique constraint
        lets exactly one win, and the loser is converted into an update rather
        than surfacing a 500.
        """
        existing = StudentService.get_profile_by_user_id(db, user_id)
        if existing is not None:
            return (
                StudentService.apply_update(
                    db, profile=existing, profile_in=profile_in, partial=False
                ),
                False,
            )

        try:
            return (
                StudentService.create_profile(
                    db, user_id=user_id, profile_in=profile_in
                ),
                True,
            )
        except IntegrityError:
            db.rollback()
            contended = StudentService.get_profile_by_user_id(db, user_id)
            if contended is None:
                # The violation was not the ownership constraint; let it surface.
                raise
            return (
                StudentService.apply_update(
                    db, profile=contended, profile_in=profile_in, partial=False
                ),
                False,
            )
