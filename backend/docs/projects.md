# Projects Module

## Overview
The Projects module is responsible for managing the core entities of the VulnScanC application. A "Project" serves as a container for security scan results, components, and historical snapshots.

## Business Logic
Projects allow users to:
- Create and name security scan contexts.
- Maintain descriptions for different scan scopes.
- Organize components and scan results under a unified identifier.

## Architecture
The module follows the standard layered architecture:

- **Routes**: `backend/app/routes/base_routes.py` handles the HTTP interface for project management.
- **Services**: `backend/app/services/api_services/projects.py` contains the orchestration logic for project operations.
- **Repository**: `backend/app/pg_repository/queries/projects.py` manages direct SQL interactions with the `projects` table.
- **Domain/Database**: The `projects` table in PostgreSQL stores the `id`, `name`, and `description`.

## Data Model
| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key |
| `name` | String | Unique name of the project |
| `description` | String | Optional description of the project |
