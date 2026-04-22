# Backend Development Guide

## Overview
The backend of VulnScanC is a layered Python application built with **Flask**. It provides a robust API for security scanning, project management, and AI-driven analysis.

## Tech Stack
- **Language/Framework**: Python (Flask)
- **Database**: PostgreSQL
- **Production Server**: Gunicorn

## Architecture
The backend follows a layered architecture to decouple business logic from external dependencies.

### Layers
- **`routes/`**: Thin controllers (Blueprints) that handle incoming HTTP requests.
- **`services/`**: Core business logic and orchestration.
- **`adapters/`**: Decouples external APIs (LLMs, etc.) from logic.
- **`pg_repository/`**: Low-level PostgreSQL interaction via `psycopg2`.
- **`repository/`**: Higher-level data access logic.
- **`domain/`**: Core entity definitions.

**Dependency Flow**: `Routes` $\rightarrow$ `Services` $\rightarrow$ `Adapters`/`Repositories` $\rightarrow$ `Database/External APIs`.

## Documentation

### Module Overview
For high-level architecture and business logic of specific modules, refer to:
- [BDU Module](./docs/bdu.md)
- [Testing Strategy](./docs/tests.md)

### API Reference
For detailed technical specifications of API endpoints, refer to the specific module documentation in the [docs/api/](./docs/api/) directory:
- [Authentication](./docs/api/authentication.md)
- [Users](./docs/api/users.md)
- [Logs](./docs/api/logs.md)
- [AI](./docs/api/ai.md)
- [Bitbake](./docs/api/bitbake.md)
- [BDU](./docs/api/bdu.md)
- [Dependency Track](./docs/api/dependency_track.md)
- [Licenses](./docs/api/licenses.md)
- [Reports](./docs/api/reports.md)

## Development Commands

### Local Development
- **Run locally**: `python backend/run.py` (port 5001).
- **Setup**: 
  - Use `backend/venv/bin/python` for running scripts.
  - `backend/requirements.txt` uses `psycopg2-binary` for easier installation. 

### Production
- **Run**: `gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"`

## Environment & Data
- **Entrypoint**: `backend/app/__init__.py` contains `create_app()`.
- **Environment Variables**: Requires variables from `backend/.env` (e.g., `POSTGRES_HOST`, `SECRET_KEY`, `JWT_SECRET_KEY`, `LDAP_*`, `DTRACK_*`, `SVACER_*`).
- **Data**: Application expects a `data/` directory in the root for logs (linked to `backend/data/`).
- **Timezone**: System is configured to `Europe/Moscow`.
- **API Proxy**: In production (Nginx), `/api/` is proxied to `http://backend:5000/`.
- **Executable Module**: Can be fetched via `http://<backend_ip>:5000/binary?action=get_file`.
