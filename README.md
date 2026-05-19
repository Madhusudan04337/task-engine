# Task Engine

Scalable async REST API built with FastAPI, PostgreSQL, and SQLAlchemy 2.0.

## Project Deliverables

- ✅ **Backend API:** Robust FastAPI implementation with a modular architecture.
- ✅ **Authentication & CRUD:** Fully functional JWT-based auth and Task management (Create, Read, Update, Delete).
- ✅ **Frontend UI:** Interactive sandbox (`frontend/index.html`) to validate and interact with the API endpoints.
- ✅ **API Documentation:** Automatically generated Interactive API docs via Swagger UI (available at `/docs`).
- ✅ **Scalability Strategy:** Comprehensive design for horizontal scaling, database optimization, and microservices readiness.

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

   ## Scalability & Roadmap

   This project is designed with a **Modular Monolith** architecture, making it ready for horizontal and vertical scaling:

   1.  **Stateless API:** The FastAPI backend is completely stateless. It can be scaled behind a Load Balancer (like Nginx or AWS ALB) to handle thousands of concurrent requests.
   2.  **Database Scalability:** 
       - **PostgreSQL Connection Pooling:** Currently using `asyncpg` which natively supports pooling.
       - **Read Replicas:** For high-traffic applications, the repository layer can be modified to route `GET` requests to a read replica.
   3.  **Caching (Redis):** While not implemented, the service layer is prepared for a Redis integration to cache frequently accessed data (e.g., user profiles or task lists).
   4.  **Security:** 
       - **RBAC:** Fully implemented role-based access control.
       - **Token Revocation:** Future roadmap includes a Redis-based blocklist for logged-out tokens.
   5.  **Microservices Ready:** The clear separation between `api`, `services`, and `repositories` allows any module (e.g., the Task service) to be easily extracted into its own microservice if needed.

