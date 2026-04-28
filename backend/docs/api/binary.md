# Binary API

## Endpoints

### GET /binary
Works with the executable module.

- **Auth**: Not required.
- **Query Params**:
  - `action=get_info` — returns information about the binary module
  - `action=get_file` — downloads the executable module (`/binary/executable_module`)

**Error Response (get_file)**
- Code: 404 Not Found — if executable module file is not found

---

### POST /binary
Builds the executable module.

- **Auth**: Not required.
- **Request Body**:
  ```json
  {
    "action": "build_binary"
  }
  ```

**Success Response**
- Code: 200 OK
- Response Body: `{"success": true}`
