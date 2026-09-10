"""Pydantic contracts for the student profile resource.

Ownership is never accepted from the client. ``user_id`` is absent from every
inbound model and is derived server-side from the authenticated bearer token,
which removes the mass-assignment path where a caller could create or move a
profile onto another account.
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

# Trims surrounding whitespace before length is checked, so a value of "   "
# is rejected rather than stored as a blank name.
NonEmptyName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=255),
]
OptionalPhone = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=32),
]


class StudentProfileBase(BaseModel):
    """Fields common to inbound and outbound representations."""

    full_name: NonEmptyName = Field(
        description="Applicant's full legal name, as it should appear on applications."
    )
    phone: OptionalPhone | None = Field(
        default=None, description="Contact number in any national or E.164 format."
    )
    education_summary: str | None = Field(
        default=None, description="Free-text summary of prior education."
    )
    writing_sample: str | None = Field(
        default=None, description="Personal statement or essay draft."
    )


class StudentProfileCreate(StudentProfileBase):
    """Payload for creating a profile.

    Deliberately carries no ``user_id``: the owner is taken from the access
    token by the router, never from the request body.
    """


class StudentProfileUpdate(BaseModel):
    """Partial update. Fields left unset are not modified."""

    full_name: NonEmptyName | None = None
    phone: OptionalPhone | None = None
    education_summary: str | None = None
    writing_sample: str | None = None


class StudentProfileResponse(StudentProfileBase):
    """Outbound representation of a persisted profile."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    created_at: datetime
