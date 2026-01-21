"""
SQLAlchemy database models for the Job Network app.
"""
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base


class Company(Base):
    """Companies you're targeting for job opportunities."""
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    careers_url = Column(String, nullable=True)
    ats_type = Column(String, nullable=True)  # 'greenhouse', 'workday', 'lever', 'custom'
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to jobs at this company
    jobs = relationship("Job", back_populates="company")


class Job(Base):
    """Job postings discovered at target companies."""
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    title = Column(String, nullable=False)
    location = Column(String, nullable=True)
    job_url = Column(String, nullable=True)
    is_remote = Column(Boolean, default=False)
    discovered_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="new")  # 'new', 'interested', 'applied', 'ignored'

    # Relationships
    company = relationship("Company", back_populates="jobs")
    matches = relationship("Match", back_populates="job")


class Connection(Base):
    """Your LinkedIn connections (people in your network)."""
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    company = Column(String, nullable=True)
    position = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    is_umd_alum = Column(Boolean, default=False)
    imported_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to matches
    matches = relationship("Match", back_populates="connection")


class Alumni(Base):
    """University alumni discovered via Apollo (not in your direct network)."""
    __tablename__ = "alumni"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    company = Column(String, nullable=True)
    position = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    school = Column(String, default="University of Maryland")
    discovered_at = Column(DateTime, default=datetime.utcnow)

    # Relationship to matches
    matches = relationship("Match", back_populates="alumni")


class Match(Base):
    """Links jobs to helpful people (connections or alumni) for outreach."""
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    connection_id = Column(Integer, ForeignKey("connections.id"), nullable=True)
    alumni_id = Column(Integer, ForeignKey("alumni.id"), nullable=True)
    match_type = Column(String, nullable=False)  # 'direct_connection', 'alumni'
    outreach_status = Column(String, default="none")  # 'none', 'queued', 'sent', 'responded'
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    job = relationship("Job", back_populates="matches")
    connection = relationship("Connection", back_populates="matches")
    alumni = relationship("Alumni", back_populates="matches")
