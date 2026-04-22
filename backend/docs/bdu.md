# BDU API

## Endpoints

### `GET /bdu`
Retrieves BDU information.

- **Auth**: Required.
- **Query Params**:
  - `action=get_info`: Returns general BDU information.
  - `action=get_component_vulns`: Returns BDU vulnerabilities for a component. Requires `component_id` and `component_type`.

### `POST /bdu`
Updates BDU data.

- **Auth**: Required.
- **Actions**:
  - `update_bdu`: `{"action": "update_bdu"}`
  - `update_vulns`: `{"action": "update_vulns"}`
- **Success Response**: `200 OK` with `{"success": true}`.
