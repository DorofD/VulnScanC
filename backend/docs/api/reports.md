# Reports API

## Endpoints

### `GET /reports`
Generates and downloads reports.

- **Auth**: Required.
- **Query Params**:
  - `report_type=osv`: Generates OSV report. Requires `snapshot_id` and optional `severities`.
  - `report_type=bdu`: Generates BDU report. Requires `snapshot_id` and optional `severities`.
  - `report_type=svacer`: Generates Svacer report. Requires `project_id`, `branch_id`, `snapshot_id`, and `project_name`.
  - `report_type=dependency_track`: Generates Dependency-Track report. Requires `project_uuid`.
  - `report_type=bitbake`: Generates Bitbake report. Requires `snapshot_id`, optional `severities`, and optional `layers`.
  - `report_type=bitbake_bdu`: Generates Bitbake-BDU report. **Note**: Currently returns a stub (`{"success": true}`), not an actual file.
