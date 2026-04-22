# Dependency Track API

## Endpoints

### `GET /dependency_track`
Retrieves Dependency Track data.

- **Auth**: Required.
- **Query Params**:
  - `action=get_projects`: Returns list of Dependency Track projects.
  - `action=get_components`: Returns components for a project. Requires `project_uuid`.
