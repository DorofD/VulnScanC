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
  - `bdu.py`: BDU (FSTEC) integration routes.
  - `bitbake.py`: Bitbake scan management.
  - `dependency_track.py`: Dependency-Track integration.
  - `licenses.py`: License management.
  - `logs.py`: Log retrieval.
  - `reports.py`: Report generation.
  - `sarif.py`: SARIF import/export.
  - `snapshots.py`: Snapshot management.
  - `svacer.py`: Svacer scan integration.
  - `users.py`: User management.
- **`services/`**: Core business logic and orchestration. This layer is subdivided into:
  - `api_services/`: Orchestration for specific API modules (e.g., `projects`, `components`, `vulnerabilities`, `binary`, `component_comments`, `bdu`, `bitbake`, `dependency_track`, `licenses`, `logs`, `reports`, `sarif`, `snapshots`, `svacer`).
  - `ai_services/`: AI-driven logic, RAG, and LLM management.
  - `bitbake/`: Bitbake-specific processing.
  - `dependencies/`: SBOM and dependency analysis.
  - `dependency_track/`: Dependency-Track API integration.
  - `fstec/`: FSTEC BDU vulnerability processing.
  - `licenses/`: License checking logic.
  - `logs.py`: Log service.
  - `notifications/`: Communication services (e.g., Mail).
  - `reports/`: Report generation (PDF, DOCX).
  - `results/`: Result handling.
  - `sarif/`: SARIF processing.
  - `search_data/`: Search data management.
  - `sec_dev_scanner/`: Specialized security scanning logic (builder, templates).
  - `svacer/`: Svacer API integration.
  - `users.py`: User service.
  - `vulnerabilities/`: Vulnerability finding logic (OSV, VulnFinder).
- **`adapters/`**: Decouples external APIs (LLMs, PDF extraction, chunking, etc.) from logic.
  - `chunker.py`: Text chunking for RAG.
  - `hasher.py`: Hashing utilities.
  - `llama_api.py`: Llama model API integration.
  - `osv_client.py`: OSV vulnerability database client.
  - `pdf_extract.py`: PDF document extraction.
- **`pg_repository/`**: Low-level PostgreSQL interaction via `psycopg2`.
  - `db_model.py`: Database model definitions.
  - `queries/`: SQL query modules.
    - `base_query.py`: Base query utilities.
    - `bdu_vulnerabilities.py`: BDU vulnerability queries.
    - `bitbake_*.py`: Bitbake-specific queries (components, licenses, projects, snapshots, vulnerabilities, comments).
    - `components.py`, `components_comments.py`: Component queries.
    - `licenses.py`: License queries.
    - `llama_nodes.py`: Llama node queries.
    - `projects.py`: Project queries.
    - `rag_chunks.py`, `rag_documents.py`: RAG document/chunk queries.
    - `snapshots.py`: Snapshot queries.
    - `users.py`: User queries.
    - `vulnerabilities.py`: Vulnerability queries.
- **`domain/`**: Core entity definitions (e.g., `user.py`).

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
- **Run locally**: `python run.py` (port 5001).
- **Setup**: 
  - Use `venv/bin/python` for running scripts.
  - `requirements.txt` uses `psycopg2-binary` for easier installation. 

### Production
- **Run**: `gunicorn -w 2 --timeout 300 -b 0.0.0.0:5000 "app:create_app()"`

## Environment & Data
- **Entrypoint**: `app/__init__.py` contains `create_app()`.
- **Environment Variables**: Requires variables from `.env` (e.g., `POSTGRES_HOST`, `SECRET_KEY`, `JWT_SECRET_KEY`, `LDAP_*`, `DTRACK_*`, `SVACER_*`).
- **Data**: Application expects a `data/` directory in the root for logs (linked to `backend/data/`).
- **Timezone**: System is configured to `Europe/Moscow`.
- **API Proxy**: In production (Nginx), `/api/` is proxied to `http://backend:5000/`.
- **Executable Module**: Can be fetched via `http://<backend_ip>:5000/binary?action=get_file`.
