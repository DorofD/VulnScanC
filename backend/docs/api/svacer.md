# Svacer API

## Endpoints

### `GET /svacer`
Retrieves Svacer-related data.

- **Auth**: Required.

**Query Params**:
- `action=get_projects`: Returns a list of Svacer projects.
- `action=get_snapshots`: Returns snapshots for a specific project and branch. Requires `project_id` and `branch_id`.

**Success Response**
- Code: 200 OK
- **Response Body**: Array of project or snapshot objects.
