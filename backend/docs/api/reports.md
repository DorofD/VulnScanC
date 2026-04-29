# Reports API

## Endpoints

### `GET /reports`
Generates and downloads reports. Most reports are returned as `.docx` files.

- **Auth**: Required.

**Query Params**:

- `report_type=osv`: Generates OSV report.
  - **Required**: `snapshot_id`
  - **Optional**: `severities`

- `report_type=bdu`: Generates BDU report.
  - **Required**: `snapshot_id`
  - **Optional**: `severities`

- `report_type=svacer`: Generates Svacer report.
  - **Required**: `project_id`, `branch_id`, `snapshot_id`, `project_name`

- `report_type=dependency_track`: Generates Dependency-Track report.
  - **Required**: `project_uuid`

- `report_type=bitbake`: Generates Bitbake report.
  - **Required**: `snapshot_id`
  - **Optional**: `severities`, `layers`

- `report_type=bitbake_bdu`: Generates Bitbake-BDU report.
  - **Note**: Currently returns a JSON stub (`{"success": true}`).

**Success Response**
- Code: 200 OK
- **Response Body**: `.docx` file (for most types) or `{"success": true}` (for `bitbake_bdu`).
