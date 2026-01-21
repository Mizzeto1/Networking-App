"""
API routes for managing LinkedIn connections.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Connection])
def list_connections(
    company: Optional[str] = None,
    is_umd_alum: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all connections, optionally filtered by company or alumni status."""
    query = db.query(models.Connection)
    if company:
        query = query.filter(models.Connection.company.ilike(f"%{company}%"))
    if is_umd_alum is not None:
        query = query.filter(models.Connection.is_umd_alum == is_umd_alum)
    connections = query.offset(skip).limit(limit).all()
    return connections


@router.post("/", response_model=schemas.Connection)
def create_connection(connection: schemas.ConnectionCreate, db: Session = Depends(get_db)):
    """Add a new connection."""
    db_connection = models.Connection(**connection.model_dump())
    db.add(db_connection)
    db.commit()
    db.refresh(db_connection)
    return db_connection


@router.get("/{connection_id}", response_model=schemas.Connection)
def get_connection(connection_id: int, db: Session = Depends(get_db)):
    """Get a specific connection by ID."""
    connection = db.query(models.Connection).filter(models.Connection.id == connection_id).first()
    if connection is None:
        raise HTTPException(status_code=404, detail="Connection not found")
    return connection


@router.delete("/{connection_id}")
def delete_connection(connection_id: int, db: Session = Depends(get_db)):
    """Delete a connection."""
    connection = db.query(models.Connection).filter(models.Connection.id == connection_id).first()
    if connection is None:
        raise HTTPException(status_code=404, detail="Connection not found")
    db.delete(connection)
    db.commit()
    return {"message": "Connection deleted"}


@router.get("/at-company/{company_name}", response_model=List[schemas.Connection])
def find_connections_at_company(company_name: str, db: Session = Depends(get_db)):
    """Find all connections who work at a specific company."""
    connections = db.query(models.Connection).filter(
        models.Connection.company.ilike(f"%{company_name}%")
    ).all()
    return connections
