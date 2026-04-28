# Comments API

## Endpoints

### GET /comments
Returns comments.

- **Auth**: Required.
- **Query Params**:
  - `type=component` + `component_id` — returns component comments (reversed order)
  - `type=vuln` — stub (not implemented)

---

### POST /comments
Adds or deletes comments.

- **Auth**: Required.
- **Request Body**:

  **Add comment**:
  ```json
  {
    "action": "add",
    "type": "component",
    "user_id": "...",
    "component_id": "...",
    "comment": "..."
  }
  ```

  **Delete comment**:
  ```json
  {
    "action": "delete",
    "type": "component",
    "comment_id": "..."
  }
  ```

  - `type=vuln` — stub (not implemented)

**Success Response**
- Code: 200 OK
- Response Body: `{"success": true}`
