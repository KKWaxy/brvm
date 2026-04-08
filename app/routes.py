"""
API routes for SGI data.
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import SGI, Review
from app.schemas import (
    SGICreate,
    SGIResponse,
    SGIUpdate,
    BulkDeleteRequest,
    ReviewCreate,
    ReviewResponse,
    ReviewUpdate,
    SGIResponseWithReviews,
)

router = APIRouter()


@router.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to SGI API", "version": "0.1.0"}


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# ============================================================================
# SGI CRUD Endpoints
# ============================================================================


@router.get("/sgi", response_model=List[SGIResponse], tags=["SGI"])
async def list_sgi(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    pays: Optional[str] = Query(None),
    nom: Optional[str] = Query(None),
):
    """
    Get list of all SGI with optional filters.

    **Parameters:**
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 1000)
    - **pays**: Filter by country
    - **nom**: Filter by name (partial match)
    """
    query = db.query(SGI)

    if pays:
        query = query.filter(SGI.pays.ilike(f"%{pays}%"))

    if nom:
        query = query.filter(SGI.nom.ilike(f"%{nom}%"))

    return query.offset(skip).limit(limit).all()


@router.get("/sgi/count", response_model=dict, tags=["SGI"])
async def count_sgi(db: Session = Depends(get_db)):
    """Get total count of SGI records."""
    count = db.query(SGI).count()
    return {"total": count}


@router.get("/sgi/countries", response_model=List[str], tags=["SGI"])
async def get_countries(db: Session = Depends(get_db)):
    """Get list of all unique countries."""
    countries = db.query(SGI.pays).distinct().filter(SGI.pays.isnot(None)).all()
    return sorted([c[0] for c in countries if c[0]])


@router.get("/sgi/by-country/{pays}", response_model=List[SGIResponse], tags=["SGI"])
async def get_sgi_by_country(
    pays: str,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """Get all SGI from a specific country."""
    sgis = db.query(SGI).filter(SGI.pays.ilike(f"%{pays}%")).offset(skip).limit(limit).all()

    if not sgis:
        raise HTTPException(status_code=404, detail=f"No SGI found for country: {pays}")

    return sgis


@router.get("/sgi/search", response_model=List[SGIResponse], tags=["SGI"])
async def search_sgi(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """
    Search SGI by name, email, or phone.

    **Parameters:**
    - **q**: Search query (minimum 1 character)
    """
    sgis = (
        db.query(SGI)
        .filter(
            (SGI.nom.ilike(f"%{q}%"))
            | (SGI.email.ilike(f"%{q}%"))
            | (SGI.telephone.ilike(f"%{q}%"))
        )
        .offset(skip)
        .limit(limit)
        .all()
    )

    return sgis


@router.get("/sgi/{sgi_id}", response_model=SGIResponse, tags=["SGI"])
async def get_sgi(sgi_id: UUID, db: Session = Depends(get_db)):
    """Get a single SGI by ID."""
    sgi = db.query(SGI).filter(SGI.id == sgi_id).first()

    if not sgi:
        raise HTTPException(status_code=404, detail="SGI not found")

    return sgi


@router.post("/sgi", response_model=SGIResponse, tags=["SGI"], status_code=201)
async def create_sgi(sgi: SGICreate, db: Session = Depends(get_db)):
    """Create a new SGI record."""
    db_sgi = SGI(**sgi.dict())
    db.add(db_sgi)
    db.commit()
    db.refresh(db_sgi)
    return db_sgi


@router.put("/sgi/{sgi_id}", response_model=SGIResponse, tags=["SGI"])
async def update_sgi(sgi_id: UUID, sgi: SGIUpdate, db: Session = Depends(get_db)):
    """Update an existing SGI record."""
    db_sgi = db.query(SGI).filter(SGI.id == sgi_id).first()

    if not db_sgi:
        raise HTTPException(status_code=404, detail="SGI not found")

    update_data = sgi.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_sgi, key, value)

    db.add(db_sgi)
    db.commit()
    db.refresh(db_sgi)
    return db_sgi


@router.patch("/sgi/{sgi_id}", response_model=SGIResponse, tags=["SGI"])
async def partial_update_sgi(sgi_id: UUID, sgi: SGIUpdate, db: Session = Depends(get_db)):
    """Partially update an SGI record."""
    db_sgi = db.query(SGI).filter(SGI.id == sgi_id).first()

    if not db_sgi:
        raise HTTPException(status_code=404, detail="SGI not found")

    update_data = sgi.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_sgi, key, value)

    db.add(db_sgi)
    db.commit()
    db.refresh(db_sgi)
    return db_sgi


@router.delete("/sgi/{sgi_id}", tags=["SGI"], status_code=204)
async def delete_sgi(sgi_id: UUID, db: Session = Depends(get_db)):
    """Delete an SGI record."""
    db_sgi = db.query(SGI).filter(SGI.id == sgi_id).first()

    if not db_sgi:
        raise HTTPException(status_code=404, detail="SGI not found")

    db.delete(db_sgi)
    db.commit()
    return None


@router.post("/sgi/bulk/delete", tags=["SGI"])
async def bulk_delete_sgi(request: BulkDeleteRequest, db: Session = Depends(get_db)):
    """Delete multiple SGI records by IDs."""
    deleted_count = db.query(SGI).filter(SGI.id.in_(request.ids)).delete()
    db.commit()
    return {"deleted": deleted_count}


# ============================================================================
# Review Endpoints
# ============================================================================


@router.get("/sgi/{sgi_id}/reviews", response_model=List[ReviewResponse], tags=["Reviews"])
async def get_reviews(
    sgi_id: UUID,
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """
    Get all reviews for a specific SGI.

    **Parameters:**
    - **sgi_id**: UUID of the SGI
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum records to return (default: 100, max: 1000)
    """
    sgi = db.query(SGI).filter(SGI.id == sgi_id).first()
    if not sgi:
        raise HTTPException(status_code=404, detail="SGI not found")

    reviews = db.query(Review).filter(Review.sgi_id == sgi_id).offset(skip).limit(limit).all()
    return reviews


@router.get("/sgi/{sgi_id}/reviews/{review_id}", response_model=ReviewResponse, tags=["Reviews"])
async def get_review(sgi_id: UUID, review_id: UUID, db: Session = Depends(get_db)):
    """Get a specific review by ID."""
    review = (
        db.query(Review)
        .filter((Review.id == review_id) & (Review.sgi_id == sgi_id))
        .first()
    )
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.post("/sgi/{sgi_id}/reviews", response_model=ReviewResponse, tags=["Reviews"])
async def create_review(
    sgi_id: UUID, review: ReviewCreate, db: Session = Depends(get_db)
):
    """
    Create a new review for an SGI.

    **Parameters:**
    - **sgi_id**: UUID of the SGI
    - **rating**: Rating from 1 to 5 stars (required)
    - **comment**: Optional comment
    - **reviewer_name**: Optional reviewer name
    - **reviewer_email**: Optional reviewer email
    """
    # Validate rating
    if review.rating < 1 or review.rating > 5:
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    # Check if SGI exists
    sgi = db.query(SGI).filter(SGI.id == sgi_id).first()
    if not sgi:
        raise HTTPException(status_code=404, detail="SGI not found")

    # Create review
    db_review = Review(
        sgi_id=sgi_id,
        rating=review.rating,
        comment=review.comment,
        reviewer_name=review.reviewer_name,
        reviewer_email=review.reviewer_email,
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@router.put("/sgi/{sgi_id}/reviews/{review_id}", response_model=ReviewResponse, tags=["Reviews"])
async def update_review(
    sgi_id: UUID, review_id: UUID, review_data: ReviewUpdate, db: Session = Depends(get_db)
):
    """Update a review."""
    review = (
        db.query(Review)
        .filter((Review.id == review_id) & (Review.sgi_id == sgi_id))
        .first()
    )
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    # Validate rating if provided
    if review_data.rating is not None and (review_data.rating < 1 or review_data.rating > 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")

    update_data = review_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(review, field, value)

    db.add(review)
    db.commit()
    db.refresh(review)
    return review


@router.delete("/sgi/{sgi_id}/reviews/{review_id}", tags=["Reviews"])
async def delete_review(sgi_id: UUID, review_id: UUID, db: Session = Depends(get_db)):
    """Delete a review."""
    review = (
        db.query(Review)
        .filter((Review.id == review_id) & (Review.sgi_id == sgi_id))
        .first()
    )
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    db.delete(review)
    db.commit()
    return {"message": "Review deleted successfully"}


@router.get("/sgi/{sgi_id}/rating-average", tags=["Reviews"])
async def get_average_rating(sgi_id: UUID, db: Session = Depends(get_db)):
    """Get average rating for a specific SGI."""
    sgi = db.query(SGI).filter(SGI.id == sgi_id).first()
    if not sgi:
        raise HTTPException(status_code=404, detail="SGI not found")

    reviews = db.query(Review).filter(Review.sgi_id == sgi_id).all()
    if not reviews:
        return {
            "sgi_id": sgi_id,
            "sgi_nom": sgi.nom,
            "average_rating": None,
            "total_reviews": 0,
        }

    average = sum(r.rating for r in reviews) / len(reviews)
    return {
        "sgi_id": sgi_id,
        "sgi_nom": sgi.nom,
        "average_rating": round(average, 2),
        "total_reviews": len(reviews),
    }


@router.get("/sgi/{sgi_id}/with-reviews", response_model=SGIResponseWithReviews, tags=["SGI"])
async def get_sgi_with_reviews(sgi_id: UUID, db: Session = Depends(get_db)):
    """Get a specific SGI with all its reviews."""
    sgi = db.query(SGI).filter(SGI.id == sgi_id).first()
    if not sgi:
        raise HTTPException(status_code=404, detail="SGI not found")
    return sgi
