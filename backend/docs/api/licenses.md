# Licenses API

## Endpoints

### `POST /licenses`
Manages licenses.

- **Auth**: Required.

**Request Body** (JSON):

- `action=check_licenses`:
  - **Required**: `project_id`

- `action=add`:
  - **Required**: `component_id`, `key`, `name`, `spdx_id`, `url`

- `action=delete`:
  - **Required**: `license_id`

**Success Response**
- Code: 200 OK
- **Response Body**: `{"success": true}`
