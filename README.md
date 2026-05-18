# Task Engine

Scalable async REST API built with FastAPI, PostgreSQL, and SQLAlchemy 2.0.

## Tech Stack

- **Backend:** FastAPI
- **Database:** PostgreSQL + asyncpg
- **ORM:** SQLAlchemy 2.0 (Async)
- **Auth:** JWT + Role-based Access Control
- **Environment:** Docker
- **Package Manager:** uv

## Project Structure

```text
task-engine/
├── backend/            # FastAPI application
│   └── app/
│       ├── api/        # Route handlers
│       ├── core/       # Config, security, logging
│       ├── db/         # Session management, base models
│       ├── models/     # SQLAlchemy models
│       ├── repositories/ # Data access layer
│       ├── schemas/    # Pydantic models (DTOs)
│       └── services/   # Business logic layer
├── frontend/           # Sandbox for API validation
├── tests/              # Pytest suite
└── docker-compose.yml  # Local infrastructure
```

## Setup

1. Clone the repository.
2. Create `.env` from `.env.example`.
3. Install dependencies using `uv`:
   ```bash
   uv sync
   ```
4. Run infrastructure:
   ```bash
   docker-compose up -d
   ```
