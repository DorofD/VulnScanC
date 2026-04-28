# Snapshots API

## Endpoints

### GET /snapshots
Returns a list of snapshots for a project.

- **Auth**: Required.
- **Query Params**:
  - `project_type` (required): `"common"` or `"bitbake"`
  - `project_id` (required): Project ID

**Error Response**
- Code: 400 Bad Request — `{"success": false, "error": "Unkown project type"}`

---

### POST /snapshots
Manages snapshots.

- **Auth**: Required.
- **Request Body**:
  - `project_type` (required): `"common"` or `"bitbake"`
  - `action`: `"delete"` — requires `snapshot_id`
  - `snapshot_id`: ID of the snapshot to delete

**Success Response**
- Code: 200 OK
- Response Body: `{"success": true}`

**Error Response**
- Code: 400 Bad Request — `{"success": false, "error": "Unkown project type"}`
