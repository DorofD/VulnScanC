# Agent Instructions for VulnScanC

## Project Structure
- `backend/`: Python (Flask) application.
- `frontend/`: React application (Webpack).
- `docker/`: Dockerfiles and Nginx configuration.

## Development Commands

### Backend
- Run locally: `python backend/run.py` (runs on port 5001).
- Production equivalent: `gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"`

### Frontend
- Development: `npm run dev` (inside `frontend/`)
- Build: `npm run build` (inside `frontend/`)

## Architecture & Quirks
- **Backend Entrypoint**: `backend/app/__init__.py` contains `create_app()`.
- **Layered Architecture**:
  - `routes/`: Thin controllers (Blueprints).
  - `services/`: Business logic and orchestration.
  - `adapters/`: Decouples external APIs (LLMs, etc.) from logic.
  - `pg_repository/`: Low-level PostgreSQL interaction via `psycopg2`.
  - `domain/`: Core entity definitions.
- **Dependency Flow**: `Routes` $\rightarrow$ `Services` $\rightarrow$ `Adapters`/`Repositories` $\rightarrow$ `Database/External APIs`.
- **Database**: Uses PostgreSQL (indicated by `pg_repository` and `psycopg2` in requirements).
- **API Proxy**: In production (Nginx), `/api/` is proxied to `http://backend:5000/`.
- **Timezone**: System is configured to `Europe/Moscow`.
- **Frontend Build**: Uses Webpack to output to `dist/`.
