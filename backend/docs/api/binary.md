# Binary API

## Endpoints

### `GET /binary`
Retrieves information or the executable module.

- **Auth**: Not required.
- **Query Params**:
  - `action=get_info`: Returns information about the binary module.
  - `action=get_file`: Downloads the executable module.

**Error Response (get_file)**
- Code: 404 Not Found — if the executable module file is not found.

---

### `POST /binary`
Builds the executable module.

- **Auth**: Not required.
- **Request Body** (JSON):
  - `action` (required): `"build_binary"`

**Success Response**
- Code: 200 OK
- Response Body: `{"success": true}`
