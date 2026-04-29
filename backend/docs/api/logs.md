# Logs API

## Endpoints

### `GET /logs`
Retrieves logs.

- **Auth**: Required.

**Query Params**:
- `action=get_json`: Returns logs in JSON format.
- `action=get_file`: Returns the log file as an attachment.

**Success Response**
- Code: 200 OK
- **Response Body**: Array of log entries (for `get_json`).

---

### `POST /logs`
Manages log files.

- **Auth**: Required.

**Request Body** (JSON):

Clear:
```json
{
  "action": "clear"
}
```

**Success Response**
- Code: 200 OK
- **Response Body**: `{"success": true}`
