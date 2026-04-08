"""
Pydantic schemas for API request/response.
"""

from typing import List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


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
    courtage: Optional[str] = None
    frais_conservation: Optional[str] = None
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
