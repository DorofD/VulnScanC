# Backend Development Guide

## Tech Stack
- **Language/Framework**: Python (Flask)
- **Database**: PostgreSQL
- **Production Server**: Gunicorn

## Architecture
The backend follows a layered architecture:
- **`routes/`**: Thin controllers (Blueprints).
- **`services/`**: Business logic and orchestration.
- **`adapters/`**: Decouples external APIs (LLMs, etc.) from logic.
- **`pg_repository/`**: Low-level PostgreSQL interaction via `psycopg2`.
- **`repository/`**: Higher-level data access logic.
- **`domain/`**: Core entity definitions.

**Dependency Flow**: `Routes` $\rightarrow$ `Services` $\rightarrow$ `Adapters`/`Repositories` $\rightarrow$ `Database/External APIs`.

## API Documentation

### Authentication
- **`POST /login`**: Authenticates a user.
  - **Request Body**: `{"login": "...", "password": "..."}`
  - **Success Response**: `200 OK` with `{"success": true, "body": {...}, "access_token": "..."}`. Sets `refresh_token` in a cookie.
  - **Error Response**: `401 Unauthorized` with `{"success": false}`.
- **`POST /refresh`**: Refreshes the access token using a valid refresh token.
  - **Success Response**: `200 OK` with `{"success": true, "access_token": "..."}`. Sets a new `refresh_token` in a cookie.

### Users
- **`GET /users`**: Retrieves a list of users.
  - **Auth**: Required (Admin role).
  - **Success Response**: `200 OK` with list of users.
- **`POST /users`**: Performs user management actions.
  - **Auth**: Required (Admin role).
  - **Actions**:
    - `add`: `{"action": "add", "login": "...", "auth_type": "...", "role": "...", "password": "..."}`
    - `change`: `{"action": "change", "id": ..., "fields_to_change": {...}}`
    - `delete`: `{"action": "delete", "id": ...}`
  - **Success Response**: `200 OK` with `{"success": true}`.

### Logs
- **`GET /logs`**: Retrieves logs.
  - **Auth**: Required.
  - **Query Params**:
    - `action=get_json`: Returns logs in JSON format.
    - `action=get_file`: Returns the log file as an attachment.
- **`POST /logs`**: Manages log files.
  - **Auth**: Required.
  - **Actions**:
    - `clear`: `{"action": "clear"}`. Deletes log files.
  - **Success Response**: `200 OK` with `{"success": true}`.

### AI
- **`GET /ai/summary`**: Returns a summary of Llama nodes.
  - **Auth**: Required.
- **`POST /ai/chat`**: Sends a chat completion request.
  - **Auth**: Required.
  - **Request Body**: `{"messages": [...], "use_rag": boolean}`
- **`GET /ai/llama_nodes`**: Retrieves all Llama nodes.
  - **Auth**: Required (Admin role).
- **`POST /ai/llama_nodes`**: Manages Llama nodes.
  - **Auth**: Required (Admin role).
  - **Actions**:
    - `add`: `{"action": "add", "values": {...}}`
    - `change`: `{"action": "change", "node_type": "...", "id": ..., "fields_to_change": {...}}`
    - `delete`: `{"action": "delete", "node_type": "...", "id": ...}`
    - `set_active`: `{"action": "set_active", "node_type": "...", "node_uuid": "..."}`
- **`GET /ai/llama_chat_nodes`**: Retrieves chat-specific Llama nodes.
  - **Auth**: Required (Admin role).
- **`POST /ai/llama_chat_nodes`**: Manages chat Llama nodes.
  - **Auth**: Required (Admin role).
  - **Actions**: `add`, `change`, `delete`.
- **`GET /ai/llama_embedding_nodes`**: Retrieves embedding-specific Llama nodes.
  - **Auth**: Required (Admin role).
- **`POST /ai/llama_embedding_nodes`**: Manages embedding Llama nodes.
  - **Auth**: Required (Admin role).
  - **Actions**: `add`, `change`, `delete`.
- **`GET /ai/rag_documents`**: Retrieves RAG documents.
  - **Auth**: Required (Admin role).
- **`POST /ai/rag_documents`**: Manages RAG documents.
  - **Auth**: Required (Admin role).
  - **Actions**:
    - `add`: Requires `file` upload (multipart/form-data).
    - `change`: `{"action": "change", "id": ..., "fields_to_change": {...}}`
    - `delete`: `{"action": "delete", "id": ...}`

### Bitbake
- **`GET /bitbake`**: Retrieves Bitbake-related data.
  - **Query Params**:
    - `action=get_projects`: Returns list of projects.
    - `action=get_components`: Returns components for a project/layer. Requires `project_id` and `layer`.
    - `action=get_vulnerabilities`: Returns vulnerabilities for a component. Requires `component_id`.
    - `action=get_component_comments`: Returns comments for a component. Requires `component_id`.
    - `action=get_vuln_comments`: Returns comments for a vulnerability. Requires `vuln_id`.
- **`POST /bitbake`**: Performs Bitbake management actions.
  - **Multipart/Form-Data**:
    - `action=upload_cve`: Uploads a CVE report. Requires `file` and `project`.
    - `action=upload_licenses`: Uploads a license manifest. Requires `file`.
  - **JSON**:
    - `add_project`: `{"action": "add_project", "project_name": "..."}`
    - `delete_project`: `{"action": "delete_project", "project_id": ...}`
    - `change_project`: `{"action": "change_project", "project_id": ..., "project_name": "..."}`
    - `add_license`: `{"action": "add_license", "component_id": ..., "license_name": "...", "recipe_name": "..."}`
    - `delete_license`: `{"action": "delete_license", "license_id": ...}`
    - `add_component_comment`: `{"action": "add_component_comment", "user_id": ..., "component_id": ..., "comment": "..."}`
    - `delete_component_comment`: `{"action": "delete_component_comment", "comment_id": ...}`
    - `add_vuln_comment`: `{"action": "add_vuln_comment", "user_id": ..., "vuln_id": ..., "comment": "..."}`
    - `delete_vuln_comment`: `{"action": "delete_vuln_comment", "comment_id": ...}`

### BDU
- **`GET /bdu`**: Retrieves BDU information.
  - **Auth**: Required.
  - **Query Params**:
    - `action=get_info`: Returns general BDU information.
    - `action=get_component_vulns`: Returns BDU vulnerabilities for a component. Requires `component_id` and `component_type`.
- **`POST /bdu`**: Updates BDU data.
  - **Auth**: Required.
  - **Actions**:
    - `update_bdu`: `{"action": "update_bdu"}`
    - `update_vulns`: `{"action": "update_vulns"}`
  - **Success Response**: `200 OK` with `{"success": true}`.

### Dependency Track
- **`GET /dependency_track`**: Retrieves Dependency Track data.
  - **Auth**: Required.
  - **Query Params**:
    - `action=get_projects`: Returns list of Dependency Track projects.
    - `action=get_components`: Returns components for a project. Requires `project_uuid`.

### Licenses
- **`POST /licenses`**: Manages licenses.
  - **Auth**: Required.
  - **Actions**:
    - `check_licenses`: `{"action": "check_licenses", "project_id": ...}`
    - `add`: `{"action": "add", "component_id": ..., "key": "...", "name": "...", "spdx_id": "...", "url": "..."}`
    - `delete`: `{"action": "delete", "license_id": ...}`
  - **Success Response**: `200 OK` with `{"success": true}`.

### Reports
- **`GET /reports`**: Generates and downloads reports.
  - **Auth**: Required.
  - **Query Params**:
    - `report_type=osv`: Generates OSV report. Requires `snapshot_id` and optional `severities`.
    - `report_type=bdu`: Generates BDU report. Requires `snapshot_id` and optional `severities`.
    - `report_type=svacer`: Generates Svacer report. Requires `project_id`, `branch_id`, `snapshot_id`, and `project_name`.
    - `report_type=dependency_track`: Generates Dependency-Track report. Requires `project_uuid`.
    - `report_type=bitbake`: Generates Bitbake report. Requires `snapshot_id`, optional `severities`, and optional `layers`.
    - `report_type=bitbake_bdu`: Generates Bitbake-BDU report.

### Licenses
- **`POST /licenses`**: Manages licenses.
  - **Auth**: Required.
  - **Actions**:
    - `check_licenses`: `{"action": "check_licenses", "project_id": ...}`
    - `add`: `{"action": "add", "component_id": ..., "key": "...", "name": "...", "spdx_id": "...", "url": "..."}`
    - `delete`: `{"action": "delete", "license_id": ...}`
  - **Success Response**: `200 OK` with `{"success": true}`.

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
