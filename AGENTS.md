# Agent Instructions for VulnScanC

## Project Structure
- `backend/`: Python (Flask) application.
- `frontend/`: React application (Webpack).
- `docker/`: Dockerfiles and Nginx configuration.

## Development Commands

### Backend
- Run locally: `python backend/run.py` (port 5001).
- Production: `gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"`
- **Setup**: 
  - Use `backend/venv/bin/python` for running scripts.
  - `backend/requirements.txt` uses `psycopg2-binary` for easier installation.
  - **Environment**: Requires variables from `backend/.env` (e.g., `POSTGRES_HOST`, `SECRET_KEY`, `JWT_SECRET_KEY`, `LDAP_*`, `DTRACK_*`, `SVACER_*`).
  - **Data**: Application expects a `data/` directory in the root for logs (linked to `backend/data/`).

### Frontend
- Development: `npm run dev` (inside `frontend/`).
- Build: `npm run build` (inside `frontend/`).
- **Environment**: Requires `frontend/.env` (if applicable).

## Architecture & Quirks
- **Backend Entrypoint**: `backend/app/__init__.py` contains `create_app()`.
- **Layered Architecture**:
  - `routes/`: Thin controllers (Blueprints).
  - `services/`: Business logic and orchestration.
  - `adapters/`: Decouples external APIs (LLMs, etc.) from logic.
  - `pg_repository/`: Low-level PostgreSQL interaction via `psycopg2`.
  - `repository/`: Higher-level data access logic.
  - `domain/`: Core entity definitions.
- **Dependency Flow**: `Routes` $\rightarrow$ `Services` $\rightarrow$ `Adapters`/`Repositories` $\rightarrow$ `Database/External APIs`.
- **Database**: Uses PostgreSQL.
- **API Proxy**: In production (Nginx), `/api/` is proxied to `http://backend:5000/`.
- **Timezone**: System is configured to `Europe/Moscow`.
- **Frontend Build**: Uses Webpack to output to `dist/`.
- **Executable Module**: Can be fetched via `http://<backend_ip>:5000/binary?action=get_file`.

