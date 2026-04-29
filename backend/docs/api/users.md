# Users API

## Endpoints

### `GET /users`
Retrieves a list of users.

- **Auth**: Required (Admin role).

**Success Response**
- Code: 200 OK
- **Response Body**: Array of user objects.

---

### `POST /users`
Performs user management actions.

- **Auth**: Required (Admin role).

**Request Body** (JSON):

Add:
```json
{
  "action": "add",
  "login": "...",
  "auth_type": "...",
  "role": "...",
  "password": "..."
}
```

Update:
```json
{
  "action": "change",
  "id": 1,
  "fields_to_change": {
    "role": "..."
  }
}
```

Delete:
```json
{
  "action": "delete",
  "id": 1
}
```

**Success Response**
- Code: 200 OK
- **Response Body**: `{"success": true}`
