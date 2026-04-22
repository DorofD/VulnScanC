# Licenses API

## Endpoints

### `POST /licenses`
Manages licenses.

- **Auth**: Required.
- **Actions**:
  - `check_licenses`: `{"action": "check_licenses", "project_id": ...}`
  - `add`: `{"action": "add", "component_id": ..., "key": "...", "name": "...", "spdx_id": "...", "url": "..."}`
  - `delete`: `{"action": "delete", "license_id": ...}`
- **Success Response**: `200 OK` with `{"success": true}`.
