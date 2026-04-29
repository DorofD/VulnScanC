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
  - `base_routes.py`: Handles core entities like Projects, Components, Vulnerabilities, Comments, and Binary management.
  - `ai.py`: Manages AI nodes and RAG documents.
  - `login.py`: Handles authentication and token refresh.
  - `users.py`, `logs.py`, etc.
- **`services/`**: Core business logic and orchestration. This layer is subdivided into:
  - `api_services/`: Orchestration for specific API modules (e.g., `projects`, `components`, `vulnerabilities`, `binary`, `component_comments`).
  - `ai_services/`: AI-driven logic, RAG, and LLM management.
  - `sec_dev_scanner/`: Specialized security scanning logic.
  - `dependencies/`: SBOM and dependency analysis.
  - `notifications/`: Communication services (e.g., Mail).
- **`adapters/`**: Decouples external APIs (LLMs, PDF extraction, chunking, etc.) from logic.
- **`pg_repository/`**: Low-level PostgreSQL interaction via `psycopg2`.
- **`repository/`**: Higher-level data access logic.
- **`domain/`**: Core entity definitions.

**Dependency Flow**: `Routes` $\rightarrow$ `Services` $\rightarrow$ `Adapters`/`Repositories` $\rightarrow$ `Database/External APIs`.

## AI & RAG Capabilities
The backend supports AI-driven analysis through:
- **LLM Integration**: Support for various Llama-based models via `adapters/llama_api.py`.
- **RAG (Retrieval-Augmented Generation)**: Ability to ingest documents (PDFs), chunk them, and store them for context-aware AI chat.
- **Node Management**: Dynamic management of chat, embedding, and general Llama nodes.

## Documentation

### Module Overview
For high-level architecture and business logic of specific modules, refer to:
- [BDU Module](./docs/bdu.md)
- [Projects Module](./docs/projects.md)
- [Testing Strategy](./docs/tests.md)

### API Reference
For detailed technical specifications of API endpoints, refer to the specific module documentation in the [docs/api/](./docs/api/) directory:
- [Authentication](./docs/api/authentication.md)
- [Users](./docs/api/users.md)
- [Logs](./docs/api/logs.md)
- [AI](./docs/api/ai.md)
- [Bitbake](./docs/api/bitbake.md)
- [BDU](./docs/api/bdu.md)
- [Projects](./docs/api/projects.md)
- [Dependency Track](./docs/api/dependency_track.md)
- [Licenses](./docs/api/licenses.md)
- [Reports](./docs/api/reports.md)
- [Snapshots](./docs/api/snapshots.md)
- [SARIF](./docs/api/sarif.md)
- [Svacer](./docs/api/svacer.md)
- [Components](./docs/api/components.md)
- [Comments](./docs/api/comments.md)
- [Vulnerabilities](./docs/api/vulnerabilities.md)
- [Binary](./docs/api/binary.md)
- [Search Data](./docs/api/search_data.md)

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
