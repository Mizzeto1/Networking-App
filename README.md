# Job Network App

A web application to help find jobs at target companies and identify people in your network who can help.

## Quick Start

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

### API Documentation

Once running, visit:
- http://localhost:8000/docs - Interactive API docs (Swagger UI)
- http://localhost:8000/redoc - Alternative API docs

## Project Structure

```
/backend
  /app
    main.py          # FastAPI app entry
    database.py      # Database connection
    models.py        # SQLAlchemy models
    schemas.py       # Pydantic schemas
    /routers
      companies.py   # Company endpoints
      jobs.py        # Job endpoints
      connections.py # Connection endpoints
      alumni.py      # Alumni endpoints
```

## Database Models

- **Company** - Target companies for job opportunities
- **Job** - Job postings at those companies
- **Connection** - Your LinkedIn connections
- **Alumni** - University alumni (discovered via Apollo)
- **Match** - Links jobs to helpful people for outreach
