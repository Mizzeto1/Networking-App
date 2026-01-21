"""
Pydantic schemas for API request/response validation.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


# --- Company Schemas ---

class CompanyBase(BaseModel):
    name: str
    careers_url: Optional[str] = None
    ats_type: Optional[str] = None  # 'greenhouse', 'workday', 'lever', 'custom'


class CompanyCreate(CompanyBase):
    pass


class Company(CompanyBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- Job Schemas ---

class JobBase(BaseModel):
    title: str
    location: Optional[str] = None
    job_url: Optional[str] = None
    is_remote: bool = False
    status: str = "new"  # 'new', 'interested', 'applied', 'ignored'


class JobCreate(JobBase):
    company_id: int


class Job(JobBase):
    id: int
    company_id: int
    discovered_at: datetime

    class Config:
        from_attributes = True


# --- Connection Schemas ---

class ConnectionBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    linkedin_url: Optional[str] = None
    is_umd_alum: bool = False


class ConnectionCreate(ConnectionBase):
    pass


class Connection(ConnectionBase):
    id: int
    imported_at: datetime

    class Config:
        from_attributes = True


# --- Alumni Schemas ---

class AlumniBase(BaseModel):
    first_name: str
    last_name: str
    email: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    linkedin_url: Optional[str] = None
    school: str = "University of Maryland"


class AlumniCreate(AlumniBase):
    pass


class Alumni(AlumniBase):
    id: int
    discovered_at: datetime

    class Config:
        from_attributes = True


# --- Match Schemas ---

class MatchBase(BaseModel):
    job_id: int
    connection_id: Optional[int] = None
    alumni_id: Optional[int] = None
    match_type: str  # 'direct_connection', 'alumni'
    outreach_status: str = "none"  # 'none', 'queued', 'sent', 'responded'


class MatchCreate(MatchBase):
    pass


class Match(MatchBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
