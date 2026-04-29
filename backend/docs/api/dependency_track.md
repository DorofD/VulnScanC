# Dependency Track API

## Endpoints

### `GET /dependency_track`
Retrieves Dependency Track data.

- **Auth**: Required.

**Query Params**:
- `action=get_projects`: Returns a list of Dependency Track projects.
- `action=get_components`: Returns components for a specific project. Requires `project_uuid`.

**Success Response**
- Code: 200 OK
- **Response Body**: Array of project or component objects.
