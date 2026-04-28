# Agent Instructions for VulnScanC

## Project Overview
VulnScanC is a security scanning application consisting of a Python (Flask) backend and a React frontend.

## Project Structure
- `backend/`: Python (Flask) application.
- `frontend/`: React application (Webpack).
- `docker/`: Dockerfiles and Nginx configuration.

## Core Workflow Rules
- **Do not interact with directories and files included in .gitignore**
- **Re-read file before each edit after failure**
- **Make smaller edits**
- **Avoid large exact-match replacements**
- **If edit fails, use surrounding unique anchors**
- **Normalize line endings**

## Architecture Overview
The project uses a layered architecture to decouple business logic from external dependencies.

- **Backend**: Follows a layered pattern (Routes $\rightarrow$ Services $\rightarrow$ Adapters/Repositories $\rightarrow$ Database/External APIs).
- **Frontend**: React-based SPA.

## Deep Dive Documentation
For detailed instructions on specific parts of the project, refer to the following:
- [Backend Documentation (backend/AGENTS.md)](backend/AGENTS.md)
- [Frontend Documentation (frontend/AGENTS.md)](frontend/AGENTS.md)
