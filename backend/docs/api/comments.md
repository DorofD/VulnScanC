# Comments API

## Endpoints

### `GET /comments`
Retrieves comments.

- **Auth**: Required (JWT).

**Query Params**:

- `type=component`:
  - Returns comments for a specific component.
  - **Required**: `component_id`
  - *Note*: Comments are returned in reversed order.

- `type=vuln`:
  - *Note*: This endpoint is currently a stub and not fully implemented.

---

### `POST /comments`
Adds or deletes comments.

- **Auth**: Required (JWT).

**Request Body** (JSON):

- `action` (required): One of `add` or `delete`.
- `type` (required): One of `component` or `vuln`.

- **Add comment** (`action=add`, `type=component`):
  - **Required**: `user_id`, `component_id`, `comment`

- **Delete comment** (`action=delete`, `type=component`):
  - **Required**: `comment_id`

- **`type=vuln` actions**:
  - *Note*: These actions are currently stubs and not fully implemented.

**Success Response**
- Code: 200 OK
- **Response Body**: `{"success": true}`
