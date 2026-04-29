# Snapshots API

## Endpoints

### `GET /snapshots`
Returns a list of snapshots for a project.

- **Auth**: Required.

**Query Params**:

- `project_type=common`:
  - **Required**: `project_id`
- `project_type=bitbake`:
  - **Required**: `project_id`

**Success Response**
- Code: 200 OK
- **Response Body**: Array of snapshot objects.

**Error Response**
- Code: 400 Bad Request — `{"success": false, "error": "Unkown project type"}`

---

### `POST /snapshots`
Manages snapshots.

- **Auth**: Required.

**Request Body** (JSON):

- `project_type=common`:
  - `action=delete`:
    - **Required**: `snapshot_id`
- `project_type=bitbake`:
  - `action=delete`:
    - **Required**: `snapshot_id`

**Success Response**
- Code: 200 OK
- **Response Body**: `{"success": true}`

**Error Response**
- Code: 400 Bad Request — `{"success": false, "error": "Unkown project type"}`
