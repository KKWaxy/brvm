"""
Database models for SGI data.
"""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
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
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
