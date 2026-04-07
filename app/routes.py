"""
API routes for SGI data.
"""

from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import SGI
from app.schemas import SGICreate, SGIResponse, SGIUpdate, BulkDeleteRequest

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
