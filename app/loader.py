"""
CSV data loader for SGI.
"""

import csv
from pathlib import Path
from app.models import SGI
from app.database import SessionLocal


def load_sgi_data():
    """Load SGI data from CSV file into database."""
    csv_file = Path(__file__).parent.parent / "data" / "brvm_sgi - brvm_sgi.csv"

    if not csv_file.exists():
        print(f"CSV file not found: {csv_file}")
        return

    db = SessionLocal()

    try:
        # Check if data already loaded
        existing_count = db.query(SGI).count()
        if existing_count > 0:
            print(f"Data already loaded: {existing_count} records found")
            return

        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            records_added = 0

            for row in reader:
                sgi = SGI(
                    nom=row.get("Nom", ""),
                    adresse=row.get("Adresse", ""),
                    bp=row.get("BP", ""),
                    pays=row.get("Pays", ""),
                    email=row.get("Email", ""),
                    fax=row.get("Fax", ""),
                    telephone=row.get("Téléphone", ""),
                    site_web=row.get("Site Web", ""),
                    agrement_crepmf=row.get("Agrément CREPMF", ""),
                    gestion_libre=row.get("Gestion libre", ""),
                    apport_initial_fcfa=row.get("Apport initial (FCFA)", ""),
                    courtage=row.get("Courtage (%)", ""),
                    frais_conservation=row.get("Frais de conservation", ""),
                    observations=row.get("Observations", ""),
                )
                db.add(sgi)
                records_added += 1

            db.commit()
            print(f"Successfully loaded {records_added} records from CSV")

    except Exception as e:
        db.rollback()
        print(f"Error loading CSV data: {e}")
    finally:
        db.close()
