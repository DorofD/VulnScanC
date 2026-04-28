# Svacer API

## Endpoints

### GET /svacer
Works with Svacer data.

- **Auth**: Required.
- **Query Params**:
  - `action=get_projects` — returns a list of Svacer projects
  - `action=get_snapshots&project_id=...&branch_id=...` — returns snapshots for a project
