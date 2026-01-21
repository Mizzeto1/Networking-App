"""
API routes for managing university alumni (discovered via Apollo).
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Alumni])
def list_alumni(
    company: Optional[str] = None,
    school: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all alumni, optionally filtered by company or school."""
    query = db.query(models.Alumni)
    if company:
        query = query.filter(models.Alumni.company.ilike(f"%{company}%"))
    if school:
        query = query.filter(models.Alumni.school.ilike(f"%{school}%"))
    alumni = query.offset(skip).limit(limit).all()
    return alumni


@router.post("/", response_model=schemas.Alumni)
def create_alumni(alumni: schemas.AlumniCreate, db: Session = Depends(get_db)):
    """Add a new alumni record."""
    db_alumni = models.Alumni(**alumni.model_dump())
    db.add(db_alumni)
    db.commit()
    db.refresh(db_alumni)
    return db_alumni


@router.get("/{alumni_id}", response_model=schemas.Alumni)
def get_alumni(alumni_id: int, db: Session = Depends(get_db)):
    """Get a specific alumni by ID."""
    alumni = db.query(models.Alumni).filter(models.Alumni.id == alumni_id).first()
    if alumni is None:
        raise HTTPException(status_code=404, detail="Alumni not found")
    return alumni


@router.delete("/{alumni_id}")
def delete_alumni(alumni_id: int, db: Session = Depends(get_db)):
    """Delete an alumni record."""
    alumni = db.query(models.Alumni).filter(models.Alumni.id == alumni_id).first()
    if alumni is None:
        raise HTTPException(status_code=404, detail="Alumni not found")
    db.delete(alumni)
    db.commit()
    return {"message": "Alumni deleted"}


@router.get("/at-company/{company_name}", response_model=List[schemas.Alumni])
def find_alumni_at_company(company_name: str, db: Session = Depends(get_db)):
    """Find all alumni who work at a specific company."""
    alumni = db.query(models.Alumni).filter(
        models.Alumni.company.ilike(f"%{company_name}%")
    ).all()
    return alumni
