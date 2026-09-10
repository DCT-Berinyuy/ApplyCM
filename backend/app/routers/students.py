"""Student profile endpoints.

Both routes are scoped to the caller. The profile is located by the account id
carried in the validated bearer token, so there is no client-supplied
identifier to tamper with and no object-level authorization check to forget.
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response, status

from app.dependencies import CurrentUser, DbSession
from app.schemas.student_profile import StudentProfileCreate, StudentProfileResponse
from app.services.student_service import StudentService

router = APIRouter(prefix="/students", tags=["students"])


@router.get(
    "/me",
    response_model=StudentProfileResponse,
    summary="Fetch the authenticated student's profile",
    responses={404: {"description": "The account has no profile yet."}},
)
def read_my_profile(
    current_user: CurrentUser,
    db: DbSession,
) -> StudentProfileResponse:
    """Return the profile belonging to the authenticated account."""
    profile = StudentService.get_profile_by_user_id(db, current_user.id)
    if profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No student profile exists for this account.",
        )
    return StudentProfileResponse.model_validate(profile)


@router.put(
    "/me",
    response_model=StudentProfileResponse,
    summary="Create or replace the authenticated student's profile",
    responses={
        200: {"description": "Existing profile replaced."},
        201: {"description": "Profile created."},
    },
)
def upsert_my_profile(
    payload: StudentProfileCreate,
    current_user: CurrentUser,
    db: DbSession,
    response: Response,
) -> StudentProfileResponse:
    """Write the caller's profile, creating it on first use.

    Ownership comes from the access token, so a caller cannot create or
    reassign a profile belonging to another account. Responds 201 when a row
    was inserted and 200 when an existing row was replaced.
    """
    profile, created = StudentService.upsert_own_profile(
        db, user_id=current_user.id, profile_in=payload
    )
    response.status_code = (
        status.HTTP_201_CREATED if created else status.HTTP_200_OK
    )
    return StudentProfileResponse.model_validate(profile)
