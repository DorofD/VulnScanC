# BDU API

## Endpoints

### `GET /bdu`
Retrieves BDU information.

- **Auth**: Required (JWT).

**Query Params**:

- `action=get_info`:
  - Returns general BDU information.

- `action=get_component_vulns`:
  - Returns BDU vulnerabilities for a component.
  - **Required**: `component_id`, `component_type`

**Success Response**
- Code: 200 OK
- **Response Body**: Object containing BDU information or vulnerability list.

**Error Response**
- Code: 400 Bad Request — `"Missing required parameters"`

---

### `POST /bdu`
Updates BDU data.

- **Auth**: Required (JWT).

**Request Body** (JSON):

- `action=update_bdu`:
  - Downloads and extracts the latest BDU XML archive from FSTEC.

- `action=update_vulns`:
  - Synchronizes BDU vulnerabilities with the local database.

**Success Response**
- Code: 200 OK
- **Response Body**: `{"success": true}`
