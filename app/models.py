"""
Database models for SGI data.
"""

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base


class SGI(Base):
    """SGI (Société de Gestion d'Intermédiaires) model."""

    __tablename__ = "sgi"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    nom = Column(String(255), index=True)
    adresse = Column(String(500))
    bp = Column(String(100))
    pays = Column(String(100), index=True)
    email = Column(String(255))
    fax = Column(String(20))
    telephone = Column(String(50))
    site_web = Column(String(255))
    agrement_crepmf = Column(String(100))
    gestion_libre = Column(String(50))
    apport_initial_fcfa = Column(String(50))
    courtage = Column(String(50))
    frais_conservation = Column(String(100))
    observations = Column(Text)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False, index=True)
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )
    # Relationship
    reviews = relationship("Review", back_populates="sgi", cascade="all, delete-orphan")


class Review(Base):
    """Review and rating model for SGI."""

    __tablename__ = "reviews"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    sgi_id = Column(UUID(as_uuid=True), ForeignKey("sgi.id", ondelete="CASCADE"), nullable=False, index=True)
    rating = Column(Integer, nullable=False, index=True)  # 1-5 stars
    comment = Column(Text)
    reviewer_name = Column(String(255))
    reviewer_email = Column(String(255))
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False, index=True)
    updated_at = Column(
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
        nullable=False,
    )
    # Relationship
    sgi = relationship("SGI", back_populates="reviews")
