# Users API

## Endpoints

### `GET /users`
Retrieves a list of users.

- **Auth**: Required (Admin role).
- **Success Response**: `200 OK` with list of users.

### `POST /users`
Performs user management actions.

- **Auth**: Required (Admin role).
- **Actions**:
  - `add`: `{"action": "add", "login": "...", "auth_type": "...", "role": "...", "password": "..."}`
  - `change`: `{"action": "change", "id": ..., "fields_to_change": {...}}`
  - `delete`: `{"action": "delete", "id": ...}`
- **Success Response**: `200 OK` with `{"success": true}`.
