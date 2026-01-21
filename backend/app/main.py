"""
FastAPI application entry point for Job Network app.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import alumni, companies, connections, jobs

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Job Network App",
    description="Find jobs and connect with people who can help",
    version="1.0.0"
)

# Configure CORS for local development
# Allows React frontend (typically on port 3000) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(companies.router, prefix="/companies", tags=["Companies"])
app.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
app.include_router(connections.router, prefix="/connections", tags=["Connections"])
app.include_router(alumni.router, prefix="/alumni", tags=["Alumni"])


@app.get("/")
def health_check():
    """Health check endpoint to verify the API is running."""
    return {"status": "healthy", "message": "Job Network API is running"}
