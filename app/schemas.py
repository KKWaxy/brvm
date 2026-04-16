"""
Pydantic schemas for API request/response.
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from app.enums import ReviewStatus


# ============================================================================
# Auth Schemas
# ============================================================================


class UserBase(BaseModel):
    """Base schema for User."""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating User."""

    password: str = Field(..., min_length=8)


class UserResponse(UserBase):
    """Schema for User response."""

    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for token response."""

    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class LoginRequest(BaseModel):
    """Schema for login request."""

    email: str
    password: str


# ============================================================================
# SGI & Review Schemas
# ============================================================================
class SGIBase(BaseModel):
    """Base schema for SGI."""

    nom: str
    adresse: Optional[str] = None
    bp: Optional[str] = None
    pays: Optional[str] = None
    email: Optional[str] = None
    fax: Optional[str] = None
    telephone: Optional[str] = None
    site_web: Optional[str] = None
    agrement_crepmf: Optional[str] = None
    gestion_libre: Optional[str] = None
    apport_initial_fcfa: Optional[str] = None
    frais_courtage: Optional[str] = None
    frais_conservation: Optional[str] = None
    frais_transfert: Optional[str] = None
    observations: Optional[str] = None


class SGICreate(SGIBase):
    """Schema for creating SGI."""

    pass


class SGIUpdate(BaseModel):
    """Schema for updating SGI."""

    nom: Optional[str] = None
    adresse: Optional[str] = None
    bp: Optional[str] = None
    pays: Optional[str] = None
    email: Optional[str] = None
    fax: Optional[str] = None
    telephone: Optional[str] = None
    site_web: Optional[str] = None
    agrement_crepmf: Optional[str] = None
    gestion_libre: Optional[str] = None
    apport_initial_fcfa: Optional[str] = None
    courtage: Optional[str] = None
    frais_conservation: Optional[str] = None
    observations: Optional[str] = None


class SGIResponse(SGIBase):
    """Schema for SGI response."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class BulkDeleteRequest(BaseModel):
    """Schema for bulk delete request."""

    ids: List[UUID]

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "ids": [
                    "550e8400-e29b-41d4-a716-446655440000",
                    "550e8400-e29b-41d4-a716-446655440001",
                ]
            }
        }


class ReviewBase(BaseModel):
    """Base schema for Review."""

    rating: int  # 1-5 stars
    comment: Optional[str] = None
    reviewer_name: Optional[str] = None
    reviewer_email: Optional[str] = None


class ReviewCreate(ReviewBase):
    """Schema for creating Review."""

    pass


class ReviewUpdate(BaseModel):
    """Schema for updating Review."""

    rating: Optional[int] = None
    comment: Optional[str] = None
    reviewer_name: Optional[str] = None
    reviewer_email: Optional[str] = None


class ReviewResponse(ReviewBase):
    """Schema for Review response."""

    id: UUID
    sgi_id: UUID
    status: ReviewStatus = ReviewStatus.PENDING
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class ReviewModerationApprove(BaseModel):
    """Schema for approving a review."""

    moderation_reason: Optional[str] = None


class ReviewModerationReject(BaseModel):
    """Schema for rejecting a review."""

    moderation_reason: str = Field(..., min_length=5, max_length=500)


class ReviewModerationResponse(ReviewBase):
    """Schema for review response with moderation info."""

    id: UUID
    sgi_id: UUID
    user_id: Optional[UUID] = None
    status: ReviewStatus
    moderation_reason: Optional[str] = None
    moderated_by: Optional[UUID] = None
    moderated_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class SGIResponseWithReviews(SGIResponse):
    """Schema for SGI response with reviews."""

    reviews: List[ReviewResponse] = []

    class Config:
        """Pydantic config."""

        from_attributes = True
